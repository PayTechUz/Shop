from django.conf import settings

from paytechuz.gateways.payme import PaymeGateway
from paytechuz.gateways.click import ClickGateway
from paytechuz.gateways.uzum.client import UzumGateway

from paytechuz.integrations.django.models import PaymentTransaction

from apps.payment.models import Invoice


class PaymentService:
    def create_payment(self, order_id, amount, provider):
        """
        Generate payment link based on order's payment type.
        """
        paytechuz_settings = settings.PAYTECHUZ

        if provider == 'payme':
            payme = PaymeGateway(
                payme_id=paytechuz_settings['PAYME']['PAYME_ID'],
                payme_key=paytechuz_settings['PAYME']['PAYME_KEY'],
                is_test_mode=paytechuz_settings['PAYME']['IS_TEST_MODE'],
            )
            return payme.create_payment(
                id=order_id,
                amount=float(amount),
                return_url="https://example.com/return"
            )

        if provider == 'click':
            click = ClickGateway(
                service_id=paytechuz_settings['CLICK']['SERVICE_ID'],
                merchant_id=paytechuz_settings['CLICK']['MERCHANT_ID'],
                merchant_user_id=paytechuz_settings['CLICK']['MERCHANT_USER_ID'],
                secret_key=paytechuz_settings['CLICK']['SECRET_KEY'],
                is_test_mode=paytechuz_settings['CLICK']['IS_TEST_MODE']
            )
            result = click.create_payment(
                id=order_id,
                amount=float(amount),
                return_url="https://example.com/return"
            )
            return result.get("payment_url")

        if provider == 'uzum':
            uzum = UzumGateway(
                api_key="17b2f7983ba2806407cb433c628e544b11d52bdf490c01e4689d9297553c8658",
                terminal_id="e62769d0-d5ce-4d4e-a405-dfa4c362ea62",
                is_test_mode=True
            )
            uzum_link = uzum.create_payment(
                id=order_id,
                amount=amount,
                return_url="https://example.com/return"
            )
            return uzum_link

        raise ValueError(f"Unsupported payment type: {provider}")

    def process_payment(self, order, status):
        """
        Update order and invoice status.
        """
        order.status = status
        order.save(update_fields=['status'])
        
        Invoice.objects.filter(order=order).update(status=status)
