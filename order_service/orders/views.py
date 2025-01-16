from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer
from rest_framework.test import APITestCase
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from django.core.cache import cache
from django.core.cache.backends.base import InvalidCacheBackendError
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')
@method_decorator(cache_page(60*15), name='dispatch')
class OrderView(APIView):
    @swagger_auto_schema(request_body=OrderSerializer, responses={201: OrderSerializer})
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, order_id):
        try:
            order = Order.objects.get(pk=order_id, is_deleted=False)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, order_id):
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        order.is_deleted = True
        order.save()
        return Response({'message': 'Order soft-deleted'}, status=status.HTTP_204_NO_CONTENT)

    def get(self, request):
        status_filter = request.GET.get('status')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        orders = Order.objects.filter(is_deleted=False)

        if status_filter:
            orders = orders.filter(status=status_filter)
        if min_price:
            orders = orders.filter(total_price__gte=min_price)
        if max_price:
            orders = orders.filter(total_price__lte=max_price)

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class OrderAPITestCase(APITestCase):
    def test_create_order(self):
        response = self.client.post('/api/orders/', {...}, format='json')
        self.assertEqual(response.status_code, 201)

class CachedOrderView(APIView):
    def get(self, request):
        try:
            cached_data = cache.get('orders_list')
            if cached_data:
                return Response(cached_data)

            # If not cached, fetch data from the database
            data = {"orders": "list of orders"}  # Replace with actual logic
            cache.set('orders_list', data, timeout=60)
            return Response(data)
        except InvalidCacheBackendError:
            print("Redis is unavailable. Returning data without caching.")
            # Return data without caching
            return Response({"orders": "list of orders"})
