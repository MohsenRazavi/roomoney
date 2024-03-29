from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from .models import Room, Item, Purchase, Note
from .forms import RoomCreateForm, RoomOptionsForm, NewPurchaseForm, ItemCreateForm, NoteCreateForm


@login_required
def room_home_view(request):
    context = {}
    user = request.user
    if request.method == 'GET':
        if (not user.full_name) or (not user.profile_photo) or (not user.biography) or (not user.phone_number):
            messages.warning(request, 'Please Complete your profile.')
        if user.has_room:
            room = user.room.first()
            members = room.member.all().order_by('-last_login')
            context = {'members': members, 'room_name': room.name, 'room_obj': room}
            return render(request, 'rooms/room_dashboard_has_room.html', context=context)
        else:
            context['form'] = RoomCreateForm()
            return render(request, 'rooms/room_dashboard_no_room.html', context=context)
    else:  # POST request
        room_form = RoomCreateForm(request.POST)
        if room_form.is_valid():
            new_room = room_form.save()
            new_room.member.add(user)
            new_room.creator = user
            new_room.save()
            user.has_room = True
            user.save()
            context['room_obj'] = new_room
            messages.success(request, 'Room created successfully.')
        return render(request, 'rooms/room_dashboard_has_room.html', context=context)


class RoomOptionsView(UserPassesTestMixin, generic.UpdateView, LoginRequiredMixin):
    model = Room
    form_class = RoomOptionsForm
    context_object_name = 'room_obj'
    template_name = 'rooms/room_options.html'
    success_url = reverse_lazy('room_dashboard')

    def post(self, request, *args, **kwargs):
        super(RoomOptionsView, self).post(self, request, *args, **kwargs)
        room = Room.objects.get(id=self.kwargs['pk'])
        for member in room.member.all():
            member.has_room = True
            member.save()
        messages.success(request, 'Settings are set successfully.')
        return redirect(reverse_lazy('room_dashboard'))

    def test_func(self):
        user = self.request.user
        room = user.room.first()
        return user == room.creator


@login_required
def add_new_purchase(request):
    user = request.user
    room = user.room.first()
    purchase_form = NewPurchaseForm()
    item_form = ItemCreateForm()
    purchase_form.fields['member'].queryset = get_user_model().objects.filter(room=room)
    purchase_form.fields['purchaser'].queryset = get_user_model().objects.filter(room=room)
    purchase_form.fields['items'].queryset = Item.objects.filter(in_purchase=False, room=room)
    items = Item.objects.filter(in_purchase=False, room=room)
    context = {'purchase_form': purchase_form, 'item_form': item_form, 'items': items, 'room_obj': room}
    if request.method == 'POST':
        user_form = NewPurchaseForm(request.POST)
        if user_form.is_valid():
            new_purchase = user_form.save(commit=False)
            new_purchase.room = room
            new_purchase.adder = user
            new_purchase.save()
            user_form.save_m2m()
            all_money = new_purchase.calculate_sum()
            shared_money = all_money / new_purchase.member.count()
            items = new_purchase.items.all()

            new_purchase.purchaser_share = all_money
            if new_purchase.purchaser in new_purchase.member.all():
                new_purchase.purchaser_share = all_money - shared_money
            new_purchase.member_share = shared_money

            new_purchase.save()

            for item in items:
                item.in_purchase = True
                item.save()

            for member in new_purchase.member.all():
                if member == new_purchase.purchaser:
                    new_purchase.purchaser.money -= shared_money
                    new_purchase.purchaser.save()
                else:
                    member.money -= shared_money
                    member.save()

            new_purchase.purchaser.money += all_money
            new_purchase.purchaser.save()

            all_items = Item.objects.all()
            for item in all_items:
                if not item.in_purchase:
                    item.delete()
            messages.success(request, 'Purchase saved successfully')
            return redirect(reverse('purchase_list', args=[room.id]))
    return render(request, 'rooms/add_new_purchase.html', context=context)


@login_required
def add_item_to_purchase(request):
    room = request.user.room.first()
    if request.method == 'POST':
        user_item = ItemCreateForm(request.POST)
        if user_item.is_valid():
            new_item = user_item.save(commit=False)
            new_item.room = room
            new_item.save()
            messages.success(request, f'{new_item.name} added to purchase successfully.')
            return redirect(reverse('new_purchase'))


class DeleteItemFromPurchase(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = Item
    success_url = reverse_lazy('new_purchase')
    success_message = 'item deleted successfully.'


@login_required
def purchase_list_view(request, pk):
    user = request.user
    room = Room.objects.get(pk=pk)
    purchases = Purchase.objects.filter(room=room, is_active=True).order_by('-created_at')
    context = {
        'room_obj': room,
        'purchases': purchases,
    }
    not_payed_count = purchases.filter(is_payed=False).count()
    messages.info(request, f'{not_payed_count} not checkout purchases.')
    if user not in room.member.all():
        return HttpResponseForbidden()
    return render(request, 'rooms/purchase_list.html', context=context)


class PurchaseDeleteView(UserPassesTestMixin, generic.DeleteView):
    model = Purchase
    template_name = 'rooms/purchase_delete.html'

    def get_context_data(self, **kwargs):
        context = super(PurchaseDeleteView, self).get_context_data(**kwargs)
        context['room_obj'] = self.request.user.room.first()
        return context

    def test_func(self):
        user = self.request.user
        purchase = get_object_or_404(Purchase, id=self.kwargs['pk'])
        room = get_object_or_404(Purchase, id=self.kwargs['pk']).room
        if purchase.is_payed:
            return False
        if user in room.member.all():
            return True

    def get_success_url(self):
        return reverse_lazy('purchase_list', args=[self.request.user.room.first().id])

    def get_queryset(self):
        queryset = Purchase.objects.filter(room=self.request.user.room.first())
        return queryset

    def post(self, request, *args, **kwargs):
        purchase = Purchase.objects.get(pk=self.kwargs['pk'])
        messages.success(self.request, f'{purchase.title} deleted successfully.')

        all_money = purchase.sum
        members = purchase.member
        shared_money = all_money / members.count()

        for member in members.all():
            if member == purchase.purchaser:
                purchase.purchaser.money += shared_money
                purchase.purchaser.save()
            else:
                member.money += shared_money
                member.save()

        purchase.purchaser.money -= all_money
        purchase.purchaser.save()
        purchase.items.all().delete()
        purchase.delete()

        user = self.request.user
        room = Room.objects.get(pk=user.room.first().id)
        purchases = Purchase.objects.filter(room=room).order_by('-created_at')
        context = {
            'room_obj': room,
            'purchases': purchases,
        }
        return redirect(reverse('purchase_list', args=[self.request.user.room.first().id]))


class RoommateOutView(UserPassesTestMixin, generic.DetailView):
    model = get_user_model()
    template_name = 'rooms/roommate_out_view.html'
    context_object_name = 'roommate'

    def test_func(self):
        user = self.request.user
        room = get_object_or_404(get_user_model(), id=self.kwargs['pk']).room.first()
        return user in room.member.all()

    def get_context_data(self, **kwargs):
        context = super(RoommateOutView, self).get_context_data(**kwargs)
        context['room_obj'] = self.request.user.room.first()

        user = self.request.user
        roommate = get_user_model().objects.filter(id=self.kwargs['pk'])
        room = user.room.first()
        purchases_member = Purchase.objects.filter(member__in=roommate, is_active=True).exclude(
            purchaser__in=roommate).order_by(
            '-created_at')
        purchases_purchaser = Purchase.objects.filter(purchaser__in=roommate, is_active=True).order_by('-created_at')
        roommate_money = get_object_or_404(get_user_model(), id=self.kwargs['pk']).money
        if roommate_money < 0:
            messages.info(self.request, 'This user is debtor.')
        if roommate_money > 0:
            messages.info(self.request, 'This user is creditor.')

        context['purchases_purchaser'] = purchases_purchaser
        context['purchases_member'] = purchases_member
        return context


@login_required
def room_delete_view(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room_obj': room}
    if request.method == 'POST':
        members = room.member.all()
        purchases = room.purchases.all()

        for member in members:
            member.has_room = False
            member.money = 0
            member.save()
        for purchase in purchases:
            for item in purchase.items.all():
                item.delete()
            purchase.delete()
        room.delete()
        messages.success(request, 'Room deleted successfully.')
        return redirect(reverse('room_dashboard'))
    else:  # GET request
        return render(request, 'rooms/room_delete.html', context=context)


@login_required
def item_list_view(request, pk):
    user = request.user
    room = Room.objects.get(pk=pk)
    items = Item.objects.filter(room=room, is_active=True).order_by('-datetime_bought')
    context = {'items': items, 'room_obj': room}
    if user not in room.member.all():
        return HttpResponseForbidden()
    return render(request, 'rooms/item_list.html', context=context)


@login_required
def checkout_view(request, pk):
    user = request.user
    room = user.room.first()
    purchase = get_object_or_404(Purchase, id=pk)
    context = {'purchase': purchase, 'room_obj': room}

    if user not in room.member.all():
        return HttpResponseForbidden

    if request.method == 'POST':

        all_money = purchase.sum
        members = purchase.member
        shared_money = all_money / members.count()

        for member in members.all():
            if member == purchase.purchaser:
                purchase.purchaser.money += shared_money
                purchase.purchaser.save()
            else:
                member.money += shared_money
                member.save()

        purchase.purchaser.money -= all_money
        purchase.purchaser.save()

        purchase.is_payed = True
        purchase.save()
        messages.success(request, f'{purchase.title} checked out successfully.')
        return redirect(reverse('purchase_list', args=[room.id]))
    else:  # GET request
        return render(request, 'rooms/checkout.html', context=context)


class NoteListView(UserPassesTestMixin, LoginRequiredMixin, generic.ListView):
    model = Note
    template_name = 'notes/note_list.html'

    def get_context_data(self, **kwargs):
        room = self.request.user.room.first()
        context = super(NoteListView, self).get_context_data(**kwargs)
        context['notes'] = Note.objects.filter(room=room).order_by('-datetime_create')
        context['room_obj'] = room
        return context

    def test_func(self):
        user = self.request.user
        room = Room.objects.get(id=self.kwargs['pk'])
        if user in room.member.all():
            return True
        return False


class NoteDeleteView(UserPassesTestMixin, LoginRequiredMixin, generic.DeleteView):
    model = Note
    template_name = 'notes/note_delete.html'

    def get_success_url(self):
        room = self.request.user.room.first()
        note = get_object_or_404(Note, id=self.kwargs['pk'])
        messages.success(self.request, f'{note.title} deleted successfully.')
        return reverse_lazy('note_list', args=[room.id])

    def test_func(self):
        user = self.request.user
        room = Note.objects.get(id=self.kwargs['pk']).room
        if user in room.member.all():
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(NoteDeleteView, self).get_context_data()
        context['room_obj'] = self.request.user.room.first()
        return context


class NoteCreateView(LoginRequiredMixin, generic.CreateView):
    model = Note
    template_name = 'notes/note_create.html'
    form_class = NoteCreateForm

    def get_context_data(self, **kwargs):
        context = super(NoteCreateView, self).get_context_data(**kwargs)
        context['room_obj'] = self.request.user.room.first()
        return context

    def post(self, request, *args, **kwargs):
        user_form = NoteCreateForm(self.request.POST)
        if user_form.is_valid():
            new_note = user_form.save(commit=False)
            new_note.user = self.request.user
            new_note.room = self.request.user.room.first()
            new_note.save()
        room = self.request.user.room.first()
        messages.success(self.request, 'Note created successfully.')
        return redirect(reverse('note_list', args=[room.id]))


@login_required
def clear_history_view(request, pk):
    user = request.user
    room = Room.objects.get(id=pk)
    purchases = room.purchases.filter(room=room, is_payed=True, is_active=True).order_by('-created_at')
    if user != room.creator:
        return HttpResponseForbidden
    if request.method == 'POST':
        for purchase in purchases:
            items = purchase.items.all()
            for item in items:
                item.is_active = False
                item.save()
            purchase.is_active = False
            purchase.save()
        messages.success(request, 'History cleared successfully.')
        return redirect(reverse('purchase_list', args=[room.id]))
    else:  # Get request
        return render(request, 'rooms/clear_history.html', context={'purchases': purchases, 'room_obj': room})
