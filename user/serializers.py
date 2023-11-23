
from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Seller, ShippingAddress

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ['first_name', 'last_name','email','username', 'password', ]  # Add other fields as needed
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
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

      



