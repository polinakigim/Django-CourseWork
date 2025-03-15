from django.forms import ModelForm

from mailing.models import Mailing, Message, Recipient


class RecipientForm(ModelForm):
    class Meta:
        model = Recipient
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите email"}
        )

        self.fields["full_name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите полное имя получателя"}
        )
        self.fields["comment"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите комментарий"}
        )


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        self.fields["subject"].widget.attrs.update({"class": "form-control", "placeholder": "Введите тему"})
        self.fields["body"].widget.attrs.update({"class": "form-control", "placeholder": "Введите текст"})


class MailingForm(ModelForm):
    class Meta:
        model = Mailing
        fields = "__all__"
