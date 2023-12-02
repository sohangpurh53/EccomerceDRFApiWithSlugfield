from django.contrib import admin
from django.urls import path, include
from user.views import (CreateUser, UserProfile,UserShipppingAddress,UserOrderDetails,UserReviews)

urlpatterns = [
   path('create/user/', CreateUser.as_view()),
   path('user/profile/', UserProfile.as_view()),
   path('user/shipping-address/', UserShipppingAddress.as_view()),
   path('user/order/', UserOrderDetails.as_view()),
   path('user/review/', UserReviews.as_view()),
]
