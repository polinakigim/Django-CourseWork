from django.shortcuts import render
from django.urls import reverse_lazy

from mailing.forms import RecipientForm
from mailing.models import Recipient
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(ListView):
    model = Recipient
    template_name = "mailing/home.html"

class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("mailing:recipient_list")

class RecipientListView(ListView):
     model = Recipient
     template_name = "recipient_list.html"

class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("mailing:recipient_list")

class RecipientDetailView(DetailView):
    model = Recipient

class RecipientDeleteView(DeleteView):
    model = Recipient
    success_url = reverse_lazy("mailing:recipient_list")