from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
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
