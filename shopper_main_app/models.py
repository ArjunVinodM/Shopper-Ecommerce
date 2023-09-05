from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
  cust_user = models.ForeignKey(User, on_delete=models.CASCADE)
  cust_mobile = models.CharField(max_length=10, default=10)
  cust_address = models.CharField(max_length=255)
  cust_locality = models.CharField(max_length=50)
  cust_city = models.CharField(max_length=50)
  cust_state = models.CharField(max_length=50)
  cust_pincode = models.IntegerField()
  
class Category(models.Model):
  category_name = models.CharField(max_length=50)
  
class Product(models.Model):
  prdt_category = models.ForeignKey(Category, on_delete=models.CASCADE)
  prdt_brand = models.CharField(max_length=50)
  prdt_title = models.CharField(max_length=100)
  prdt_description = models.CharField(max_length=355)
  prdt_selling_price = models.IntegerField()
  prdt_discounted_price = models.IntegerField()
  prdt_image = models.ImageField(upload_to='image/')
  
class Cart(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField(default = 1)

class OrderPlaced(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField(default=1)
  ordered_date = models.DateTimeField(auto_now_add=True)
  status = models.CharField(max_length=100, default='pending')
  
  @property
  def total_cost(self):
      return self.quantity * self.product.prdt_discounted_price
      
# class Address(models.Model):
#   user_address = models.ForeignKey(User, on_delete=models.CASCADE)
#   first_name = models.CharField(max_length=55)
#   last_name = models.CharField(max_length=55)
#   mobile = models.CharField(max_length=10, default=10)
#   address = models.CharField(max_length=255)
#   locality = models.CharField(max_length=50)
#   city = models.CharField(max_length=50)
#   state = models.CharField(max_length=50)
#   pincode = models.IntegerField()
  
  
  