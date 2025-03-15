from django.core.exceptions import ValidationError
from django.forms import ModelForm

from mailing.models import Recipient

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