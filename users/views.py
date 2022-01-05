from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UserCreationForm


class RegisterView(CreateView):
	form_class = UserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'users/register.html'