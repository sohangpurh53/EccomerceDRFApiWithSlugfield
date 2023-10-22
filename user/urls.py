from django.contrib import admin
from django.urls import path, include
from user.views import (CreateUser, UserProfile,UserShipppingAddress)

urlpatterns = [
   path('create/user/', CreateUser.as_view()),
   path('user/profile/', UserProfile.as_view()),
   path('user/shipping-address/', UserShipppingAddress.as_view()),
]
