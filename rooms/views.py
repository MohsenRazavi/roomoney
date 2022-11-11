from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy, reverse

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
            context['text'] = 'this one has not room'
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
    form_class = RoomOptionsForm
    context_object_name = 'room_obj'
    template_name = 'rooms/room_options.html'
    success_url = reverse_lazy('room_dashboard')


@login_required
def add_new_purchase(request):
    user = request.user
    room = user.room.first()
    purchase_form = NewPurchaseForm()
    item_form = ItemCreateForm()
    purchase_form.fields['member'].queryset = get_user_model().objects.filter(room=room)
    purchase_form.fields['purchaser'].queryset = get_user_model().objects.filter(room=room)
    purchase_form.fields['items'].queryset = Item.objects.filter(in_purchase=False)
    items = Item.objects.filter(in_purchase=False)
    context = {'purchase_form': purchase_form, 'item_form': item_form, 'items': items, 'room_obj': room}
    if request.method == 'POST':
        user_form = NewPurchaseForm(request.POST)
        if user_form.is_valid():
            print(request.POST)
            new_purchase = user_form.save(commit=False)
            new_purchase.room = room
            new_purchase.save()
            user_form.save_m2m()

            items = new_purchase.items.all()

            for item in items:
                item.in_purchase = True
                item.save()

            all_items = Item.objects.all()
            for item in all_items:
                if not item.in_purchase:
                    item.delete()

            return redirect(reverse('room_dashboard'))
    return render(request, 'rooms/add_new_purchase.html', context=context)


@login_required
def add_item_to_purchase(request):
    if request.method == 'POST':
        user_item = ItemCreateForm(request.POST)
        if user_item.is_valid():
            user_item.save()
            return redirect(reverse('new_purchase'))


class DeleteItemFromPurchase(generic.DeleteView, LoginRequiredMixin):
    model = Item
    success_url = reverse_lazy('new_purchase')


def purchase_list_view(request, pk):
    room = Room.objects.get(pk=pk)
    purchases = Purchase.objects.filter(room=room)

    purchase_sum = 0
    # for purchase in purchases:
    #     for item in purchase.items.all():
    #         purchase_sum += item.price
    context = {
        'room_obj': room,
        'purchases': purchases,
        'sum': purchase_sum,
    }
    return render(request, 'rooms/purchase_list.html', context=context)



