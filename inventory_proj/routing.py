from django.urls import path
from inventory import websocket_consumer

websocket_urlpatterns = [
    path('ws/orders/<str:username>/', websocket_consumer.OrderStatusConsumer.as_asgi()),
]