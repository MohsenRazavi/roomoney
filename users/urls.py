from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.SignupLoginView.as_view(), name='login_to_home'),
]
