from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from paytechuz.gateways.payme import PaymeGateway
from paytechuz.gateways.click import ClickGateway
from paytechuz.gateways.atmos import AtmosGateway
from paytechuz.integrations.django.models import PaymentTransaction
from django.conf import settings

from .serializers import OrderCreateSerializer, PaymentLinkResponseSerializer


class CreateOrderAPIView(APIView):
    """API endpoint for creating orders with payment integration."""

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        order = serializer.save()

        try:
            payment_url = generate_payment_link(order)
            order.payment_url = payment_url
            order.save()

            # Return payment link response
            response_data = {
                'order_id': order.id,
                'payment_url': payment_url,
                'payment_type': order.payment_type,
                'amount': order.amount,
                'status': order.status
            }

            response_serializer = PaymentLinkResponseSerializer(response_data)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            order.delete()  # Clean up the order if payment link creation fails
            return Response(
                {'error': f'Error creating payment link: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )


def generate_payment_link(order):
    """Generate payment link based on order's payment type."""
    paytechuz_settings = settings.PAYTECHUZ

    if order.payment_type == 'payme':
        payme = PaymeGateway(
            payme_id=paytechuz_settings['PAYME']['PAYME_ID'],
            payme_key=paytechuz_settings['PAYME']['PAYME_KEY'],
            is_test_mode=paytechuz_settings['PAYME']['IS_TEST_MODE'],
        )
        return payme.create_payment(
            id=order.id,
            amount=float(order.amount),
            return_url="https://example.com/return"
        )

    if order.payment_type == 'click':
        click = ClickGateway(
            service_id=paytechuz_settings['CLICK']['SERVICE_ID'],
            merchant_id=paytechuz_settings['CLICK']['MERCHANT_ID'],
            merchant_user_id=paytechuz_settings['CLICK']['MERCHANT_USER_ID'],
            secret_key=paytechuz_settings['CLICK']['SECRET_KEY'],
            is_test_mode=paytechuz_settings['CLICK']['IS_TEST_MODE']
        )
        result = click.create_payment(
            id=order.id,
            amount=float(order.amount),
            return_url="https://example.com/return"
        )
        return result.get("payment_url")

    if order.payment_type == 'atmos':
        try:
            # Get PayTechUZ Atmos configuration
            paytechuz_config = getattr(settings, 'PAYTECHUZ', {})
            atmos_config = paytechuz_config.get('ATMOS', {})

            # Initialize Atmos gateway with PayTechUZ configuration
            atmos_gateway = AtmosGateway(
                consumer_key=atmos_config.get('CONSUMER_KEY'),
                consumer_secret=atmos_config.get('CONSUMER_SECRET'),
                store_id=atmos_config.get('STORE_ID'),
                terminal_id=atmos_config.get('TERMINAL_ID'),
                is_test_mode=atmos_config.get('IS_TEST_MODE', True)
            )

            # Create payment
            payment_result = atmos_gateway.create_payment(
                account_id=order.id,
                amount=float(order.amount)
            )

            # Create PaymentTransaction record
            PaymentTransaction.create_transaction(
                gateway=PaymentTransaction.ATMOS,
                transaction_id=payment_result['transaction_id'],
                account_id=str(order.id),
                amount=order.amount
            )

            return payment_result['payment_url']

        except Exception as e:
            raise ValueError(f"Atmos payment error: {str(e)}")

    raise ValueError(f"Unsupported payment type: {order.payment_type}")
