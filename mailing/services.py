from django.core.cache import cache

from config.settings import CACHE_ENABLED
from mailing.models import Mailing, Message, Recipient


def get_recipients_from_cache():
    if not CACHE_ENABLED:
        return Recipient.objects.all()
    key = 'recipient_list'
    recipients = cache.get(key)
    if recipients is not None:
        return recipients
    recipients = Recipient.objects.all()
    cache.set(key, recipients)
    return recipients


def get_messages_from_cache():
    if not CACHE_ENABLED:
        return Message.objects.all()
    key = 'recipient_list'
    messages = cache.get(key)
    if messages is not None:
        return messages
    messages = Message.objects.all()
    cache.set(key, messages)
    return messages


def get_mailings_from_cache():
    if not CACHE_ENABLED:
        return Mailing.objects.all()
    key = 'recipient_list'
    mailings = cache.get(key)
    if mailings is not None:
        return mailings
    mailings = Mailing.objects.all()
    cache.set(key, mailings)
    return mailings
