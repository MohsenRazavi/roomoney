from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def room_home_view(request):
    user = request.user
    context = {}
    if user.has_room:
        room = user.room.first()
        members = room.member.all()
        context = {'members': members, 'room_name': room.name}
    else:
        context['text'] = 'this one has not room'
    return render(request, 'rooms/room_dashboard.html', context=context)

