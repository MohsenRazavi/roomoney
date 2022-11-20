from django.views import generic
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from .models import CustomUser
from .forms import UserUpdateForm


class UserUpdateView(generic.UpdateView):
    model = CustomUser
    form_class = UserUpdateForm
    success_url = reverse_lazy('room_dashboard')
    template_name = 'users/profile_update.html'

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['room_obj'] = self.request.user.room.first()
        return context


def leave_room_view(request):
    user = request.user
    room = user.room.first()
    user.money = 0

    if request.method == 'POST':
        if user.has_room:
            room = user.room.first()
            user.has_room = False
            room.member.remove(user)
            user.save()
            room.save()
        return redirect(reverse('room_dashboard'))
    else: # GET request
        return render(request, 'users/leave_room.html', context={'room_obj': room})

