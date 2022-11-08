from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import RoomCreateForm


@login_required
def room_home_view(request):
    context = {}
    user = request.user
    if request.method == 'GET':
        if user.has_room:
            room = user.room.first()
            members = room.member.all()
            context = {'members': members, 'room_name': room.name}
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
