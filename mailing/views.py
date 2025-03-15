from django.shortcuts import render
from mailing.models import Recipient
from django.views.generic import ListView

class HomeView(ListView):
    model = Recipient
    template_name = "home.html"