from rest_framework import serializers
from api.models import Cart ,Category, Order, Product, ShippingAddress, Seller, Review, OrderItem, CartItem, AboutUs, ProductImage
from user.serializers import  UserSerializer,UserProfileSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']




class ProductsImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"

class ProductSerializers(serializers.ModelSerializer):
    images =  ProductsImageSerializers(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True
    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'category', 
                 "images", "uploaded_images", 'seller'
                  ]

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        product = Product.objects.create(**validated_data)

        for image in uploaded_images:
            ProductImage.objects.create(product=product, image=image)

        return product







class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id','product','image']

class ProductSerializer(serializers.ModelSerializer):
    first_image = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'shipping_fee', 'stock', 'category', 'seller', 'first_image']
    def get_first_image(self, obj):
        # Get the first image for the product
        first_image = ProductImage.objects.filter(product=obj).first()

        # Serialize the first image
        if first_image:
            return first_image.image.url
        else:
            return None




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
    user = UserProfileSerializer()
    class Meta:
        model = Order
        fields = ['id','user', 'total_amount','is_paid', 'shipping_address', 'created_at']

class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    product = ProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id','order', 'product','quantity']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','product', 'user','rating', 'comment', 'created_at']


class ShippingAddressSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
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


class UserOrderDetailsSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    product = ProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id','order', 'product','quantity']