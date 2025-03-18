from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from config import settings
from mailing.forms import MailingForm, MessageForm, RecipientForm
from mailing.models import Mailing, MailingAttempt, Message, Recipient
from mailing.services import (get_mailings_from_cache, get_messages_from_cache,
                              get_recipients_from_cache)


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

    def get_queryset(self):
        return get_recipients_from_cache()


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

    def get_queryset(self):
        return get_messages_from_cache()


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")


# Контроллеры для модели Рассылки
class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy("mailing:mailing_list")


class MailingDetailView(DetailView):
    model = Mailing


class MailingListView(ListView):
    model = Mailing
    template_name = "mailing_list.html"

    def get_queryset(self):
        return get_mailings_from_cache()


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")


class SendMailingView(View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)

        # Создаем попытку рассылки сразу
        attempt = MailingAttempt.objects.create(
            mailing=mailing,
            status="не успешно",
            server_response="Попытка отправки"
        )

        if mailing.is_blocked:
            attempt.server_response = "Рассылка заблокирована. Отправка невозможна."
            attempt.save()
            return HttpResponseForbidden("Рассылка заблокирована и не может быть отправлена.")

        recipients = mailing.recipients.all()

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

        attempt.server_response = "\n".join(responses)
        if successful_recipients:
            attempt.status = "успешно"
        else:
            attempt.status = "не успешно"

        attempt.save()

        if successful_recipients:
            mailing.status = "завершена"
        else:
            mailing.status = "не отправлена"

        mailing.save()

        return HttpResponse(
            "Рассылка завершена!"
        )


class BlockMailingView(LoginRequiredMixin, View):
    def get(self, request, mailing_id):
        mailing = get_object_or_404(Mailing, id=mailing_id)
        return render(request, "mailing/mailing_block.html", {"mailing": mailing})

    def post(self, request, mailing_id):
        mailing = get_object_or_404(Mailing, id=mailing_id)

        if not request.user.has_perm("mailing.can_disable_mailings"):
            return HttpResponseForbidden("У вас нет прав для блокировки рассылки.")

        is_blocked = request.POST.get("is_blocked") == "on"  # Теперь работает правильно
        mailing.is_blocked = is_blocked
        mailing.save()

        return redirect("mailing:mailing_list")


class MailingAttemptListView(ListView):
    model = MailingAttempt
    template_name = "mailing/mailing_attempt_list.html"
