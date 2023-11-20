from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from dashboard.views import (  
                              CreateProductViewset,UpdateProduct,DeleteProduct,
                              HomepageProduct,ListProduct,SingleProduct,
                              ProductImageCreate, UdpateProductImage, DeleteProductImage,ProductImageView,
                              CreateCategory, UpdateCategory, DeleteCategory, ListCategory,
                              ListCartview, DeleteCartview, UpdateCartview, CreateCartview,AddToCartView, ReduceQuantityView, RemoveCartItemView,
                              CreateCartItem, UpdateCartItem, DeleteCartItem, ListCartItem,
                              CreateOrder, UpdateOrder, DeleteOrder, ListOrder,
                              CreateOrderItem, UpdateOrderItem, DeleteOrderItem, ListOrderItem,AdminListProduct,
                              CreateReview, UpdateReview, DeleteReview, ListReview,
                              CreateShippingAddress, UpdateShippingAddress, DeleteShippingAddress, ListShippingAddress,
                              CreateSeller,ListSeller,SerachProduct,
                              
                              )
router = DefaultRouter()
router.register(r'create/product', CreateProductViewset, basename='product')

   
 

urlpatterns = [
   #category urls
   path('create/category/', CreateCategory.as_view(), name='create-category' ),
   path('update/category/<slug:slug>/', UpdateCategory.as_view(), name='update-category' ),
   path('delete/category/<slug:slug>/', DeleteCategory.as_view(), name='delete-category' ),
   path('list/category/', ListCategory.as_view(), name='list-category' ),



   #product urls
   path('', include(router.urls)),
   path('update/product/<slug:slug>/', UpdateProduct.as_view(), name='update-product' ),
   path('delete/product/<slug:slug>/', DeleteProduct.as_view(), name='delete-product' ),
   path('list/product/', ListProduct.as_view(), name='list-product' ),
   path('admin/list/product/', AdminListProduct.as_view(), name='list-product' ),
   path('homepage/', HomepageProduct.as_view(), name='homepage-product' ),
    path('product/<slug:slug>/', SingleProduct.as_view(), name='list-product' ),

   #product Images
   path('products/images/<slug:product_slug>/', ProductImageView.as_view(), name='product-image-list'),
   path('create/product/image/', ProductImageCreate.as_view() , name='create-product-image'),
   path('update/product/image/<slug:slug>/', UdpateProductImage.as_view() , name='update-product-image'),
   path('delete/product/image/<int:pk>/', DeleteProductImage.as_view() , name='delete-product-image'),




   path('create/seller/', CreateSeller.as_view(), name='' ),
   path('list/seller/', ListSeller.as_view(), name='' ),

   #cart urls
   path('create/cart/', CreateCartview.as_view(), name='-cart'),
   path('update/cart/<slug:slug>/', UpdateCartview.as_view(), name='-cart'),
   path('delete/cart/<slug:slug>/', DeleteCartview.as_view(), name='-cart'),
   path('list/cart/', ListCartview.as_view(), name='-cart'),

    path('add_to_cart/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove_cart_item/<int:cart_item_id>/', RemoveCartItemView.as_view(), name='remove_cart_item'),
    path('reduce_quantity/<int:cart_item_id>/', ReduceQuantityView.as_view(), name='reduce_quantity'),

   #cartitem urls
   path('create/cart-item/', CreateCartItem.as_view() ,name='create-cart-item'),
   path('update/cart-item/<slug:slug>/', UpdateCartItem.as_view() ,name='update-cart-item'),
   path('delete/cart-item/<slug:slug>/', DeleteCartItem.as_view() ,name='delete-cart-item'),
   path('list/cart-item/', ListCartItem.as_view() ,name='list-cart-item'),

   #order urls
   path('create/order/', CreateOrder.as_view() , name='create-order'),
   path('update/order/<slug:slug>/', UpdateOrder.as_view() , name='update-order'),
   path('delete/order/<slug:slug>/', DeleteOrder.as_view() , name='delete-order'),
   path('list/order/', ListOrder.as_view() , name='list-order'),

   #order-item urls
   path('create/order-item/', CreateOrderItem.as_view() ,name='create-order-item'),
   path('update/order-item/<slug:slug>/', UpdateOrderItem.as_view() ,name='update-order-item'),
   path('delete/order-item/<slug:slug>/', DeleteOrderItem.as_view() ,name='delete-order-item'),
   path('list/order-item/', ListOrderItem.as_view() ,name='list-order-item'),

   #reviews urls
   path('create/review/', CreateReview.as_view() , name='create-review'),
   path('update/review/<slug:slug>/', UpdateReview.as_view() , name='update-review'),
   path('delete/review/<slug:slug>/', DeleteReview.as_view() , name='delete-review'),
   path('list/review/', ListReview.as_view() , name='list-review'),

   #shippingaddress urls
   path('create/shipping-address/', CreateShippingAddress.as_view() , name='create-shipping-address'),
   path('update/shipping-address/<slug:slug>/', UpdateShippingAddress.as_view() , name='update-shipping-address'),
   path('delete/shipping-address/<slug:slug>/', DeleteShippingAddress.as_view() , name='delete-shipping-address'),
   path('list/shipping-address/', ListShippingAddress.as_view() , name='lis-shipping-address'),
  

  #search result
  path('product/', SerachProduct.as_view())

]
