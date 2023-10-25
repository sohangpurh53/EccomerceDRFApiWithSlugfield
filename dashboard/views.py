from django.shortcuts import get_object_or_404, render, redirect

from api.models import (Cart ,Category, Order, Product,
                         ShippingAddress, Seller, Review,
                           OrderItem, CartItem, AboutUs, ProductImage)

from dashboard.serializers import (CategorySerializer, ProductSerializer,CartItemSerializer,HomepageProductImageSerializer,
                                    OrderSerializer, OrderItemSerializer,ReviewSerializer,ListProductSerializer,
                                    ShippingAddressSerializer,ListCategorySerializer,
                                    ProductImageSerializer,CartSerializer)

from user.serializers import SellerSerializer

from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, ListAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib import messages
import json

# Create your views here.

class ProductPerPagePermisson(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 1000



#category CURD
class CreateCategory(CreateAPIView):
    serializer_class = CategorySerializer


class UpdateCategory(RetrieveUpdateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        slug = self.kwargs.get('slug')
        return Category.objects.get(slug=slug)

class DeleteCategory(RetrieveDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        slug = self.kwargs.get('slug')
        return Category.objects.get(slug=slug)

class ListCategory(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = ListCategorySerializer





#product CURD
class CreateProduct(CreateAPIView):
    serializer_class = ProductSerializer

class UpdateProduct(RetrieveUpdateAPIView):
    serializer_class = ProductSerializer
    # permission_classes = [IsAdminUser]
    
    def get_object(self):
        slug = self.kwargs.get('slug')
        return Product.objects.get(slug=slug)
    
class DeleteProduct(RetrieveDestroyAPIView):
    serializer_class = ProductSerializer
    # permission_classes = [IsAdminUser]

    def get_object(self):
        slug = self.kwargs.get('slug')
        return Product.objects.get(slug=slug)

class HomepageProduct(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = HomepageProductImageSerializer
    pagination_class = ProductPerPagePermisson

class ListProduct(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ListProductSerializer

class SingleProduct(RetrieveAPIView):
    serializer_class = ProductSerializer
    def get_object(self):
        slug = self.kwargs.get('slug')  # Get the slug from the URL parameters
        return Product.objects.get(slug=slug)


#productimage CURD
class ProductImageCreate(CreateAPIView):
    serializer_class = ProductImageSerializer



class UdpateProductImage(RetrieveUpdateAPIView):
    serializer_class = ProductImageSerializer
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return ProductImage.objects.get(slug=slug)



    

class DeleteProductImage(RetrieveDestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer



class ProductImageView(ListAPIView):
    serializer_class = ProductImageSerializer

    def get_queryset(self):
        product_slug = self.kwargs.get('product_slug')
        return ProductImage.objects.filter(product__slug=product_slug)
    





#seller CURD
class CreateSeller(CreateAPIView):
    serializer_class = SellerSerializer

class ListSeller(ListAPIView):
    queryset = Seller.objects.all() 
    serializer_class = SellerSerializer


#cart CURD
class CreateCartview(ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get the user's cart
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
        except Cart.DoesNotExist:
            # If the cart does not exist, create a new one
            cart = Cart.objects.create(user=request.user)
            cart_items = []

        # Serialize the cart items
        cart_item_serializer = CartItemSerializer(cart_items, many=True)

        # Calculate the subtotal and total shipping fees
        subtotal = 0
        total_shipping_fee = 0
        for item in cart_items:
            item_total_price = item.product.price * item.quantity
            subtotal += item_total_price
            total_shipping_fee += item.product.shipping_fee * item.quantity

        # Calculate the total amount including shipping fees
        total_amount = subtotal + total_shipping_fee

        # Prepare data for response
        response_data = {
            'cart': cart.id,  # Assuming you want to send the cart ID
            'cart_items': cart_item_serializer.data,
            'subtotal': subtotal,
            'shipping_fee': total_shipping_fee,
            'total_amount': total_amount,
        }

        return Response(response_data, status=status.HTTP_200_OK)

#add cart items
class AddToCartView(APIView):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        if request.user.is_authenticated:
            user = request.user
            cart, created = Cart.objects.get_or_create(user=user)
            cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

            if item_created:
                return  Response({'message': 'Item added to cart.'})
            else:
                cart_item.quantity += 1
                cart_item.save()
                return  Response({'message': 'Item quantity updated.'})

            # if request.GET.get('buy_now') == 'true':
            #     return redirect('checkout')
            # else:
            #     return redirect('productpage', product_id=product_id)
        else:
            return Response({'message': 'User is not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)
#remove
class RemoveCartItemView(APIView):
    def delete(self,request, cart_item_id):
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#reduce
class ReduceQuantityView(APIView):
    def patch(self, request, cart_item_id):
        cart_item = get_object_or_404(CartItem, id=cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
           

        return Response({'message': 'Quantity updated successfully.'}, status=status.HTTP_200_OK)


class UpdateCartview(RetrieveUpdateAPIView):
    serializer_class = CartSerializer

    def get_object(self):
        slug = self.kwargs.get('slug')
        return Cart.objects.get(slug=slug)

class DeleteCartview(RetrieveDestroyAPIView):
    serializer_class = CartSerializer

    def get_object(self):
        slug = self.kwargs.get('slug')
        return Cart.objects.get(slug=slug)

class ListCartview(ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


#cartItem CURD
class CreateCartItem(CreateAPIView):
    serializer_class = CartItemSerializer

class UpdateCartItem(RetrieveUpdateAPIView):
    serializer_class = CartItemSerializer

    def get_object(self):
        slug = self.kwargs.get('slug')
        return CartItem.objects.get(slug=slug)

class DeleteCartItem(RetrieveDestroyAPIView):
    serializer_class = CartItemSerializer
    def get_object(self):
        slug = self.kwargs.get('slug')
        return CartItem.objects.get(slug=slug)

class ListCartItem(ListAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


#order CURD
class CreateOrder(ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        created_at = request.data.get('created_at')
    
        address_choice = request.data.get('address_choice')

        if address_choice == 'new':
            address = request.data.get('address')
            city = request.data.get('city')
            state = request.data.get('state')
            country = request.data.get('country')
            postal_code = request.data.get('postal_code')

            shipping_address, created = ShippingAddress.objects.get_or_create(
                user=user,
                address=address,
                city=city,
                state=state,
                country=country,
                postal_code=postal_code
            )
        else:
            chosen_address = ShippingAddress.objects.get(id=int(address_choice))
            shipping_address = chosen_address

        subtotal = 0
        total_shipping_fee = 0
        for item in cart_items:
            item_total_price = item.product.price * item.quantity
            subtotal += item_total_price
            total_shipping_fee += item.product.shipping_fee * item.quantity
        total_amount = subtotal + total_shipping_fee

        shipping_address_serializer = ShippingAddressSerializer(shipping_address)
        shipping_address_data = shipping_address_serializer.data
        formatted_address = f"{shipping_address_data['address']}, {shipping_address_data['city']}, {shipping_address_data['state']}, {shipping_address_data['country']} {shipping_address_data['postal_code']}"

       
        


        order = Order.objects.create(
            user=user, created_at=created_at, total_amount=total_amount, shipping_address=formatted_address, is_paid=True
        )

        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity
            )
        cart_item_serializer = CartItemSerializer(cart_items, many=True)
        cart_item_data = cart_item_serializer.data
        

        context = {
            'cart_items': cart_item_data,
            # 'old_shipping_addresses': old_shipping_addresses,
            'shipping_address': shipping_address_data,
            'total_amount': total_amount,
        }
        cart_items.delete()

        return Response(context, status=status.HTTP_201_CREATED)

    



    

class UpdateOrder(RetrieveUpdateAPIView):
    serializer_class = OrderSerializer

    def get_object(self):
        slug = self.kwargs.get('slug')
        return Order.objects.get(slug=slug)

class DeleteOrder(RetrieveDestroyAPIView):
    serializer_class = OrderSerializer

    def get_object(self):
        slug = self.kwargs.get('slug')
        return Order.objects.get(slug=slug)

class ListOrder(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

#orderItem CURD
class CreateOrderItem(CreateAPIView):
    serializer_class = OrderItemSerializer

class UpdateOrderItem(RetrieveUpdateAPIView):
    serializer_class = OrderItemSerializer

    def get_object(self):
        slug = self.kwargs.get('slug')
        return OrderItem.objects.get(slug=slug)

class DeleteOrderItem(RetrieveDestroyAPIView):
    serializer_class = OrderItemSerializer

    def get_object(self):
        slug = self.kwargs.get('slug')
        return OrderItem.objects.get(slug=slug)

class ListOrderItem(ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


#Review CURD
class CreateReview(CreateAPIView):
    serializer_class = ReviewSerializer

class UpdateReview(RetrieveUpdateAPIView):
    serializer_class = ReviewSerializer

    def get_object(self):
        slug = self.kwargs.get('slug')
        return Review.objects.get(slug=slug)

class DeleteReview(RetrieveDestroyAPIView):
    serializer_class = ReviewSerializer

    def get_object(self):
        slug = self.kwargs.get('slug')
        return Review.objects.get(slug=slug)

class ListReview(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


#ShippingAddress CURD
class CreateShippingAddress(CreateAPIView):
    serializer_class = ShippingAddressSerializer
    permission_classes = [IsAuthenticated] 

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    

class UpdateShippingAddress(RetrieveUpdateAPIView):
    serializer_class = ShippingAddressSerializer

    def get_object(self):
        slug = self.kwargs.get('slug')
        return ShippingAddress.objects.get(slug=slug)

class DeleteShippingAddress(RetrieveDestroyAPIView):
    serializer_class = ShippingAddressSerializer

    def get_object(self):
        slug = self.kwargs.get('slug')
        return ShippingAddress.objects.get(slug=slug)

class ListShippingAddress(ListAPIView):
    serializer_class = ShippingAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return  ShippingAddress.objects.filter(user=user)
