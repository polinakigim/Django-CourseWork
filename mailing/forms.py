from django.forms import ModelForm

from mailing.models import Mailing, Message, Recipient


class RecipientForm(ModelForm):
    class Meta:
        model = Recipient
        exclude = ['owner']

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
        exclude = ['owner']


    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        self.fields["subject"].widget.attrs.update({"class": "form-control", "placeholder": "Введите тему"})
        self.fields["body"].widget.attrs.update({"class": "form-control", "placeholder": "Введите текст"})


class MailingForm(ModelForm):
    class Meta:
        model = Mailing
        fields = ['message', 'recipients']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields["message"].queryset = Message.objects.filter(owner=user)
            self.fields["recipients"].queryset = Recipient.objects.filter(owner=user)
