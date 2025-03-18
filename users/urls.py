from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.views import UserCreateView, email_verification, UserListView, BlockUserView
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("email_confirm/<str:token>/", email_verification, name="email_confirm"),

    path("user_list/", UserListView.as_view(), name="user_list"),
    path("user_block/<int:user_id>", BlockUserView.as_view(), name="user_block"),

]
