from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path, reverse_lazy

from users.apps import UsersConfig
from users.views import (BlockUserView, UserCreateView, UserDetailView,
                         UserListView, UserProfileUpdateView,
                         email_verification)

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("user_profile/<int:pk>/", UserDetailView.as_view(), name="user_profile"),
    path("user_edit/<int:pk>/", UserProfileUpdateView.as_view(), name="user_edit"),
    path("email_confirm/<str:token>/", email_verification, name="email_confirm"),

    path("user_list/", UserListView.as_view(), name="user_list"),
    path("user_block/<int:user_id>", BlockUserView.as_view(), name="user_block"),

    path("password_reset/", PasswordResetView.as_view(template_name="users/password_reset_form.html",
                                                      email_template_name="users/password_reset_email.html",
                                                      success_url=reverse_lazy("users:password_reset_done")),
         name="password_reset"),
    path("password_reset/done/", PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
         name="password_reset_done"),
    path("password_reset/<uidb64>/<token>/",
         PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html",
                                          success_url=reverse_lazy("users:password_complete")),
         name="password_reset_confirm"),

    path("password_reset/complete/",
         PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
         name="password_complete"),

]
