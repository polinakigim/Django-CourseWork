import os

from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from django.utils import timezone

from mailing.models import Mailing, MailingAttempt


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('pk', type=int, help='ID рассылки')

    def handle(self, *args, **kwargs):
        pk = kwargs['pk']
        mailing = get_object_or_404(Mailing, id=pk)
        recipients = mailing.recipients.all()

        statistics = {
            'successful_attempts': 0,
            'failed_attempts': 0,
            'attempts': []
        }

        for recipient in recipients:
            attempt = MailingAttempt(timestamp=timezone.now(), mailing=mailing)

            try:
                subject = mailing.message.subject
                message = mailing.message.body
                from_email = os.getenv('EMAIL_HOST_USER')
                send_mail(subject, message, from_email, [recipient.email])

                attempt.status = 'успешно'
                statistics['successful_attempts'] += 1

            except Exception as e:
                attempt.status = 'не успешно'
                attempt.server_response = str(e)
                statistics['failed_attempts'] += 1

            attempt.save()

            statistics['attempts'].append({
                'recipient': recipient.email,
                'status': attempt.status,
                'reply': attempt.server_response,
            })

        self.stdout.write(self.style.SUCCESS(
            f'Рассылка завершена. Успешные попытки: {statistics["successful_attempts"]}, '
            f'Неуспешные попытки: {statistics["failed_attempts"]}'))
