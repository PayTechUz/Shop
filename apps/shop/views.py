from django.db import transaction

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.payment.models import Invoice
from apps.payment.service import PaymentService
from apps.shop.serializers import OrderCreateSerializer, PaymentLinkResponseSerializer


class CreateOrderAPIView(APIView):
    """API endpoint for creating orders with payment integration."""

    @transaction.atomic
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        order = serializer.save()

        try:
            # Create invoice for the order
            invoice = Invoice.objects.create(
                order=order,
                amount=order.amount,
                status='pending'
            )

            payment_service = PaymentService()
            payment_url = payment_service.create_payment(
                order_id=order.id,
                amount=order.amount,
                provider=order.payment_type
            )
            order.payment_url = payment_url
            order.save()

            response_data = {
                'invoice_id': invoice.id,
                'payment_url': payment_url,
            }

            response_serializer = PaymentLinkResponseSerializer(response_data)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'error': f'Error creating payment link: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )


