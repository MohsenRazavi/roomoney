from django.shortcuts import render

from allauth.account.forms import LoginForm, SignupForm
from allauth.account.views import SignupView


class SignupLoginView(SignupView):
    template_name = 'users/login_to_home.html'

    def get_context_data(self, **kwargs):
        context = super(SignupLoginView, self).get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        return context

# def signup_login_view(request):
#     context = {
#         'signup_form': SignupForm(),
#         'login_form': LoginForm(),
#     }
#     return render(request, 'users/login_to_home.html', context=context)
