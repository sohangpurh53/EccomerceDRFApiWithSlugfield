from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
import uuid
# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True) 

    def save(self, *args, **kwargs):
        existing_category = Category.objects.filter(name=self.name)
        if existing_category.exists():
            # Category with the same name already exists, handle it here
            # For example, you might want to update the existing category
            existing_category.update(slug=slugify(self.name))
        else:
            self.slug = slugify(self.name)
            super().save(*args, **kwargs)


    def __str__(self):
        return self.name


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    mobile_no = models.IntegerField()
    

    def __str__(self):
        return self.company_name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(default=0)  # Add remaining stock field
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, unique=True) 

  
    def save(self, *args, **kwargs):
        if self.id: 
            super().save(*args, **kwargs)
        else: 
            self.slug = slugify(self.name)
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    


        
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images')
    slug = models.SlugField(default=uuid.uuid4, editable=False, unique=True)


    def __str__(self):
        return self.product.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        existing_cart = Cart.objects.filter(slug=self.slug)
        if existing_cart.exists():
            # Cart with the same slug already exists, handle it here
            # For example, you might want to update the existing cart
            existing_cart.update(created_at=self.created_at)
        else:
            self.slug = slugify(self.user.username + ' Cart')
            super().save(*args, **kwargs)


    def __str__(self):
        return f"Cart {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    slug = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)



    def __str__(self):
        return f"CartItem {self.product.name}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    shipping_address = models.CharField(max_length=500, null=True, blank=True)
    



    def __str__(self):
        return f"Order {self.user.username}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    slug = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)



    def __str__(self):
        return f"OrderItem {self.product.name}"
    

   



class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[
            MinValueValidator(1, message='Rating should not be less than 1.'),
            MaxValueValidator(5, message='Rating should not be greater than 5.')
        ])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

   

   

    def __str__(self):
        return f"Review for {self.product}"


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    mobile_no = models.IntegerField()
    



    def __str__(self):
        return f"Shipping Address for {self.user.username}"

class AboutUs(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    description = models.TextField()
    brand_logo = models.ImageField(upload_to='brand_logo', default=False)
    
    def __str__(self):
        return self.description