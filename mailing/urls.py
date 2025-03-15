from django.urls import path, include
from mailing.apps import MailingConfig
from mailing.views import HomeView, RecipientCreateView, RecipientListView, RecipientDetailView, RecipientUpdateView, RecipientDeleteView

app_name = MailingConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('recipient_list/', RecipientListView.as_view(), name='recipient_list'),
    path('recipient_create/', RecipientCreateView.as_view(), name='recipient_create'),
    path('recipient_detail/<int:pk>/', RecipientDetailView.as_view(), name='recipient_detail'),
    path('recipient_update/<int:pk>/', RecipientUpdateView.as_view(), name='recipient_update'),
    path('recipient_delete/<int:pk>/', RecipientDeleteView.as_view(), name='recipient_delete'),
]
