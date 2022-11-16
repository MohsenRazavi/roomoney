from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.db.models import Q

from .models import Room, Item, Purchase
from .forms import RoomCreateForm, RoomOptionsForm, NewPurchaseForm, ItemCreateForm


@login_required
def room_home_view(request):
    context = {}
    user = request.user
    if request.method == 'GET':
        if user.has_room:
            room = user.room.first()
            members = room.member.all()
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
            new_room.save()
            user.has_room = True
            user.save()
        return render(request, 'rooms/room_dashboard_has_room.html', context=context)


class RoomOptionsView(generic.UpdateView, LoginRequiredMixin):
    model = Room
    # form_class = RoomOptionsForm
    context_object_name = 'room_obj'
    template_name = 'rooms/room_options.html'
    success_url = reverse_lazy('room_dashboard')

    def get_form(self, *args, **kwargs):
        room = Room.objects.get(id=self.kwargs['pk'])
        form = RoomOptionsForm(instance=room)
        # form.fields['member'].queryset = get_user_model().objects.filter(room=room)
        return form


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
            new_purchase.save()
            user_form.save_m2m()
            all_money = new_purchase.calculate_sum()
            shared_money = all_money / new_purchase.member.count()
            items = new_purchase.items.all()

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
            return redirect(reverse('new_purchase'))


class DeleteItemFromPurchase(generic.DeleteView, LoginRequiredMixin):
    model = Item
    success_url = reverse_lazy('new_purchase')


@login_required
def purchase_list_view(request, pk):
    room = Room.objects.get(pk=pk)
    purchases = Purchase.objects.filter(room=room).order_by('-created_at')
    context = {
        'room_obj': room,
        'purchases': purchases,
    }
    return render(request, 'rooms/purchase_list.html', context=context)


class PurchaseDeleteView(generic.DeleteView):
    model = Purchase
    template_name = 'rooms/purchase_delete.html'

    def get_context_data(self, **kwargs):
        context = super(PurchaseDeleteView, self).get_context_data(**kwargs)
        context['room_obj'] = self.request.user.room.first()
        return context

    def get_success_url(self):
        return reverse_lazy('purchase_list', args=[self.request.user.room.first().id])

    def get_queryset(self):
        queryset = Purchase.objects.filter(room=self.request.user.room.first())
        return queryset

    def post(self, request, *args, **kwargs):
        purchase = Purchase.objects.get(pk=self.kwargs['pk'])

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
        return render(request, 'rooms/purchase_list.html', context=context)


class RoommateOutView(generic.DetailView):
    model = get_user_model()
    template_name = 'rooms/roommate_out_view.html'
    context_object_name = 'roommate'

    def get_context_data(self, **kwargs):
        context = super(RoommateOutView, self).get_context_data(**kwargs)
        context['room_obj'] = self.request.user.room.first()

        user = self.request.user
        roommate = get_user_model().objects.filter(id=self.kwargs['pk'])
        room = user.room.first()
        purchases = Purchase.objects.filter(Q(member__in=roommate) | Q(purchaser__in=roommate)).order_by('-created_at')
        context['purchases'] = purchases
        return context

