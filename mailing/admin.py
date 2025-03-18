from django.contrib import admin

from mailing.models import Mailing, MailingAttempt, Message, Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "full_name", "comment")
    list_filter = ("full_name",)
    search_fields = (
        "full_name",
        "email",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "body")
    list_filter = ("subject",)
    search_fields = ("subject",)


@admin.register(Mailing)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "message")
    list_filter = ("status",)
    search_fields = ("status",)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "status")
    list_filter = ("status",)
    search_fields = ("status",)
