
from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Seller, ShippingAddress
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ['first_name', 'last_name','email','username', 'password', ]  # Add other fields as needed
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        username = validated_data.get('username')

        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(**validated_data)

        # Send an email to the new user
        subject = 'Welcome to our platform'
        message = 'Thank you for signing up!'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
                
        html_message = render_to_string('signupemail.html')
        send_mail(subject, message, from_email, recipient_list, html_message=html_message)

        return user

class SellerSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Include the UserSerializer

    class Meta:
        model = Seller
        fields = ['id','user', 'company_name', 'address', 'mobile_no']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        seller = Seller.objects.create(user=user, **validated_data)
        return seller
    
class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ['id', 'address', 'city', 'state', 'country', 'postal_code', 'mobile_no']
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name','email','username',  'is_staff', 'is_superuser', 'is_active']

      



