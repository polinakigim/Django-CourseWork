from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password1')

    exclude = (
        "is_blocked",
        "last_login",
        "is_superuser",
        "is_staff",
        "groups",
        "user_permissions",
        "date_joined",
        "is_active",
        "token",
    )


class UserProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'avatar', 'phone_number', 'country']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
