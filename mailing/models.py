import logging

from django.db import models
from users.models import User


class Recipient(models.Model):
    email = models.CharField(max_length=50, unique=True, help_text='Email получателя рассылки')
    full_name = models.CharField(max_length=100, verbose_name='ФИО', help_text='Полное имя получателя рассылки')
    comment = models.TextField('Введите комментарий о получателе')
    owner = models.ForeignKey(User, verbose_name="Владелец", blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'
        ordering = ['email', ]
        permissions = [
            ("can_view_all_recipient", "can view all recipient"),
        ]

    def __str__(self):
        return f"{self.full_name}"


class Message(models.Model):
    subject = models.CharField(max_length=50, help_text='Тема сообщения')
    body = models.TextField('Тело сообщения')
    owner = models.ForeignKey(User, verbose_name="Владелец", blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщений"
        ordering = ["subject"]
        permissions = [
            ("can_view_all_messages", "can view all messages"),
        ]


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('завершена', 'Завершена'),
        ('создана', 'Создана'),
        ('запущена', 'Запущена'),
    ]
    first_shipment = models.DateTimeField(auto_now_add=True, help_text='Дата и время первой отправки рассылки')
    last_shipment = models.DateTimeField(auto_now_add=True, help_text='Дата и время окончания отправки рассылки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='создана')
    message = models.OneToOneField(Message, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Recipient, verbose_name="Получатели")
    owner = models.ForeignKey(User, verbose_name="Владелец", blank=True, null=True, on_delete=models.SET_NULL)

    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return f"Рассылка с {self.recipients.count()} получателями"

    def block_mailing(self):
        self.is_blocked = True
        self.save()
        logging.info(f"Рассылка {self.pk} заблокирована пользователем")

    def unblock_mailing(self):
        self.is_blocked = False
        self.save()
        logging.info(f"Рассылка {self.pk} разблокирована пользователем")

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['message', 'status', ]
        permissions = [
            ("can_view_all_mailings", "can view all mailings"),
            ("can_disable_mailings", "can disable mailings"),
        ]


class MailingAttempt(models.Model):
    STATUS_CHOICES = [
        ('успешно', 'Успешно'),
        ('не успешно', 'Не успешно'),
    ]

    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время попытки")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    server_response = models.TextField(blank=True, null=True, verbose_name="Ответ почтового сервера")
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='attempts', verbose_name="Рассылка")

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = "Попытка"
        verbose_name_plural = "Попытки"
        ordering = ["status"]
        permissions = [
            ("can_view_all_mailings_attempts", "can view all mailings attempts"),
        ]
