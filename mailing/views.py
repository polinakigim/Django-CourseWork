from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from config import settings
from mailing.forms import MailingForm, MessageForm, RecipientForm
from mailing.models import Mailing, MailingAttempt, Message, Recipient
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(ListView):
    model = Recipient
    template_name = "mailing/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_mailings"] = Mailing.objects.count()
        context["active_mailings"] = Mailing.objects.filter(
            Q(status='запущена') | Q(status='завершена')
        ).count()
        context["unique_recipients"] = Recipient.objects.count()
        return context


# Контроллеры для модели Получателя рассылки
class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("mailing:recipient_list")


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    success_url = reverse_lazy("mailing:recipient_list")


class RecipientDetailView(DetailView):
    model = Recipient


class RecipientListView(ListView):
    model = Recipient
    template_name = "recipient_list.html"


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("mailing:recipient_list")


# Контроллеры для модели Сообщение
class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("mailing:message_list")


class MessageDetailView(DetailView):
    model = Message


class MessageListView(ListView):
    model = Message
    template_name = "message_list.html"


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")


# Контроллеры для модели Рассылки
class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy("mailing:maling_list")


class MailingDetailView(DetailView):
    model = Mailing


class MailingListView(ListView):
    model = Mailing
    template_name = "mailing_list.html"


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")


class SendMailingView(View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        recipients = mailing.recipients.all()

        # Создание попытки рассылки
        attempt = MailingAttempt.objects.create(
            mailing=mailing,
            status="не успешно"
        )

        successful_recipients = []
        failed_recipients = []
        responses = []

        for recipient in recipients:
            try:
                send_mail(
                    mailing.message.subject,
                    mailing.message.body,
                    settings.EMAIL_HOST_USER,
                    [recipient.email],
                    fail_silently=False,
                )
                successful_recipients.append(recipient)
                responses.append(f"Успешно: {recipient.email}")
            except Exception as e:
                failed_recipients.append(recipient)
                responses.append(f"Неуспешно: {recipient.email} - {str(e)}")

        # Обновление попытки рассылки
        attempt.server_response = "\n".join(responses)
        attempt.status = "успешно" if len(failed_recipients) == 0 else "не успешно"
        attempt.save()

        # Обновление статуса рассылки
        if len(successful_recipients) == len(recipients):
            mailing.status = "завершена"
        else:
            mailing.status = "запущена"  # Если были ошибки, можно оставить статус "создана"
        mailing.save()

        return HttpResponse(
            f"Рассылка завершена! Успешно: {len(successful_recipients)}, Неуспешно: {len(failed_recipients)}"
        )
