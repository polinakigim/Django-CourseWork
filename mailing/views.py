from django.shortcuts import render
from django.urls import reverse_lazy

from mailing.forms import RecipientForm, MessageForm, MailingForm
from mailing.models import Recipient, Message, Mailing
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(ListView):
    model = Recipient
    template_name = "mailing/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_mailings"] = Mailing.objects.count()
        context["active_mailings"] = Mailing.objects.filter(status='запущена').count()
        context["unique_recipients"] = Recipient.objects.count()
        return context


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

# Контроллеры для модели Сообщение
class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy("mailing:maling_list")


class MailingDetailView(DetailView):
    model = Mailing


class MailingListView(ListView):
    model = Mailing
    template_name = "mailing_list.html"


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")