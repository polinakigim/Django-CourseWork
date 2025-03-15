from django.urls import path, include
from mailing.apps import MailingConfig
from mailing.views import HomeView

app_name = MailingConfig.name

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
]
