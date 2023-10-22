from rest_framework import serializers
from api.models import Cart ,Category, Order, Product, ShippingAddress, Seller, Review, OrderItem, CartItem, AboutUs, ProductImage



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'shipping_fee', 'stock', 'category', 'seller']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id','product','image']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id','user', 'created_at']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = CartItem
        fields = ['id','cart', 'product','quantity']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','user', 'total_amount','is_paid', 'shipping_address']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id','order', 'product','quantity']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','product', 'user','rating', 'comment', 'created_at']


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ['id','user', 'address','city', 'state', 'country', 'postal_code', 'mobile_no']



#homepage
class HomepageProductImageSerializer(serializers.ModelSerializer):
    first_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'slug', 'name', 'description', 'price', 'shipping_fee', 'stock', 'category', 'seller', 'first_image']

    def get_first_image(self, obj):
        first_image = ProductImage.objects.filter(product=obj).first()
        if first_image:
            return first_image.image.url
        return None
    
#update and delete serializers
# category
class ListCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name', 'slug']


class  ListProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'shipping_fee', 'stock', 'category', 'seller', 'slug']


# class DeleteProductImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductImage
#         fields = ['id','product','image', 'slug']