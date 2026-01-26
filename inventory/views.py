from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from inventory.authentication import JWTAuthenticationWithoutUserDB
from .serializers import OrderSerializer, OrderItemSerializer
from .order_queue import order_queue

from .models import Order

# Create your views here.
@api_view(["POST"])
@authentication_classes([JWTAuthenticationWithoutUserDB])
@permission_classes([IsAuthenticated])
def save_order(request):
    username = request.headers.get("X-Username")
    
    # Handle list of orders
    orderSerialiser = OrderSerializer(
        data=request.data,
        many=True,
        context={'user_id': request.user.id, 'username': username}
    )
    
    if orderSerialiser.is_valid():
        orders = orderSerialiser.save() 
        for order in orders:
            order_queue.put(order.id)

        return Response(
            data={"message": "Order Created"}, 
            status=status.HTTP_201_CREATED
        )
    
    return Response(
        data={"error": orderSerialiser.errors}, 
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(["GET"])
@authentication_classes([JWTAuthenticationWithoutUserDB])
@permission_classes([IsAuthenticated])
def get_user_orders(request):
    try:
        username = request.headers.get("X-Username")
        orders = Order.objects.filter(username=username).order_by('created_on')
        orderSerialiser = OrderItemSerializer(orders, many=True)
        print(orderSerialiser.data)
        return Response(data={"orders": orderSerialiser.data}, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"Error fetching orders: {str(e)}")
        return Response(
            data={"error": "Failed to fetch orders"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )