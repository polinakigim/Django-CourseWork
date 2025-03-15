from django.shortcuts import render
from django.urls import reverse_lazy

from mailing.forms import RecipientForm, MessageForm
from mailing.models import Recipient, Message
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(ListView):
    model = Recipient
    template_name = "mailing/home.html"


#Контроллеры для модели Получателя рассылки
class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("mailing:recipient_list")

class RecipientDeleteView(DeleteView):
    model = Recipient
    success_url = reverse_lazy("mailing:recipient_list")

class RecipientDetailView(DetailView):
    model = Recipient

class RecipientListView(ListView):
     model = Recipient
     template_name = "recipient_list.html"

class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("mailing:recipient_list")


# Контроллеры для модели Сообщение
class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy("mailing:message_list")


class MessageDetailView(DetailView):
    model = Message


class MessageListView(ListView):
    model = Message
    template_name = "message_list.html"


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")