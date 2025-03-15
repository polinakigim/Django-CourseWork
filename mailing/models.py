from django.db import models
from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
import logging


class Recipient(models.Model):
    email = models.CharField(max_length=50, unique=True, help_text='Email получателя рассылки')
    full_name = models.CharField(max_length=100, verbose_name='ФИО', help_text='Полное имя получателя рассылки')
    comment = models.TextField('Введите комментарий о получателе')

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'
        ordering = ['email', ]

    def __str__(self):
        return f"{self.full_name}"


class Message(models.Model):
    subject = models.CharField(max_length=50, help_text='Тема сообщения')
    body = models.TextField('Тело сообщения')

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщений"
        ordering = ["subject"]


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
    is_success = models.BooleanField(default=False)

    def __str__(self):
        return f"Рассылка с {self.recipients.count()} получателями"

    # def send_email_to_recipients(self):
    #     from_email = EMAIL_HOST_USER
    #     subject = self.message.subject
    #     message = self.message.body
    #     recipient_list = [recipient.email for recipient in self.recipients.all()]

        # try:
        #     send_mail(subject, message, from_email, recipient_list)
        #     self.attempts.create(status='успешно', server_response="Email успешно отправлен")
        #     self.is_success = True
        #     self.save()
        #     logging.info(f"Рассылка {self.pk} успешно отправлена")
        # except Exception as e:
        #     error_message = str(e)
        #     self.attempts.create(status='не успешно', server_response=error_message)
        #     self.is_success = False
        #     self.save()
        #     logging.error(f"Ошибка при отправке рассылки {self.pk}: {error_message}")

    def unsuccess_mailing(self):
        self.is_blocked = True
        self.save()
        logging.info(f"Рассылка {self.pk} заблокирована пользователем")

    def success_mailing(self):
        self.is_blocked = False
        self.save()
        logging.info(f"Рассылка {self.pk} разблокирована пользователем")

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['message', 'status', ]
        permissions = [
            ('can_unpublish', 'Can unpublish '),
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
