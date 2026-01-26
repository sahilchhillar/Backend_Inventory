from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.save_order, name='order-list'),
    path('orders/user/', views.get_user_orders, name='get_user_orders'),
]