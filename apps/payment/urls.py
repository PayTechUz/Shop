# urls.py
from django.urls import path

from apps.payment.views import PaymeWebhookView, ClickWebhookView, UzumWebhookView


urlpatterns = [
    path('payments/payme/webhook/', PaymeWebhookView.as_view(), name='payme_webhook'),
    path('payments/click/webhook', ClickWebhookView.as_view(), name='click_webhook'),
    path('payments/uzum/webhook/<str:action>/', UzumWebhookView.as_view(), name='uzum_webhook')
]
