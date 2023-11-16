from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from user.serializers import UserSerializer, UserProfileSerializer,ShippingAddressSerializer
from dashboard.serializers import UserOrderDetailsSerializer
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from api.models import Cart ,Category, Order, Product, ShippingAddress, Seller, Review, OrderItem, CartItem, AboutUs, ProductImage
from rest_framework import status
from django.http import Http404
# Create your views here.
class CreateUser(CreateAPIView):
    serializer_class = UserSerializer

class UserProfile(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class UserShipppingAddress(ListAPIView):
    serializer_class = ShippingAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ShippingAddress.objects.filter(user=user)
  
class UserOrderDetails(ListAPIView):
    serializer_class = UserOrderDetailsSerializer

    def get_queryset(self):
        # Check if user is authenticated
        if self.request.user.is_authenticated:
            user = self.request.user  
            orders = Order.objects.filter(user=user)
            order_items = OrderItem.objects.filter(order__in=orders)
            return order_items
        else:
            # Handle the case where the user is not authenticated
            raise Http404("User is not authenticated or has no orders")
    

    
       



class BlacklistRefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'refresh_token required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            RefreshToken(refresh_token).blacklist()
            return Response({'message': 'refresh token blacklisted successfully'}, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
