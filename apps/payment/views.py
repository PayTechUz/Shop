from django.db import transaction

from paytechuz.integrations.django.views import BaseUzumWebhookView
from paytechuz.integrations.django.views import BasePaymeWebhookView
from paytechuz.integrations.django.views import BaseClickWebhookView


from apps.shop.models import Order
from apps.payment.service import PaymentService


payment_service = PaymentService()


class PaymeWebhookView(BasePaymeWebhookView):
    @transaction.atomic
    def successfully_payment(self, params, transaction_obj):
        order = Order.objects.get(id=transaction_obj.account_id)
        payment_service.process_payment(order, 'paid')

    @transaction.atomic
    def cancelled_payment(self, params, transaction_obj):
        order = Order.objects.get(id=transaction_obj.account_id)
        payment_service.process_payment(order, 'cancelled')


class ClickWebhookView(BaseClickWebhookView):
    @transaction.atomic
    def successfully_payment(self, params, transaction_obj):
        order = Order.objects.get(id=transaction_obj.account_id)
        payment_service.process_payment(order, 'paid')

    @transaction.atomic
    def cancelled_payment(self, params, transaction_obj):
        order = Order.objects.get(id=transaction_obj.account_id)
        payment_service.process_payment(order, 'cancelled')


class UzumWebhookView(BaseUzumWebhookView):
    def get_check_data(self, params, transaction_obj):
        return {
            "order": {
                "id": transaction_obj.order.id,
                "amount": transaction_obj.order.amount,
                "status": transaction_obj.order.status,
            }
        }

    @transaction.atomic
    def successfully_payment(self, params, transaction_obj):
        order = Order.objects.get(id=transaction_obj.account_id)
        payment_service.process_payment(order, 'paid')

    @transaction.atomic
    def cancelled_payment(self, params, transaction_obj):
        order = Order.objects.get(id=transaction_obj.account_id)
        payment_service.process_payment(order, 'cancelled')
