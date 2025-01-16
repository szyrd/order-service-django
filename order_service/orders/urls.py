from django.urls import path
from .views import OrderView

urlpatterns = [
    path('', OrderView.as_view(), name='order-list-create'),  # List all orders, create a new order
    path('<int:order_id>/', OrderView.as_view(), name='order-detail-update-delete'),  # Update, delete, or get a specific order
]

