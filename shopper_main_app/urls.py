# from django.urls import path
# from .views import *


# urlpatterns = [
#   path('', home)
# ]


from django.urls import path
from . import views


urlpatterns = [
  path('', views.home, name='home'),
  path('login', views.signin, name='login'),
  path('profile', views.view_profile, name='profile'),
  path('update_profile/<int:pk>', views.profile , name='update_profile'),
  path('register', views.signup, name='register'),
  path('change_pass', views.change_pass, name='change_pass'),
  path('customer_pass_change', views.pass_change, name='customer_pass_change'),
  
  path('cart', views.show_cart , name='cart'),
  path('addcart', views.add_cart, name='addcart'),
  path('remove_product/<int:pk>', views.remove_cart, name='remove_product'),
  path('buy-now/<int:pk>', views.buy_now, name='buy-now'),
  path('checkout', views.checkout, name='checkout'),
  path('order', views.orders, name='order'),
  path('order_placed', views.ordered ,name='order_placed'),
  path('buy_placed/<int:pk>', views.buy_order ,name='buy_placed'),
  
  # path('add_address', views.address, name='add_address'),
  # path('address_insert', views.insert_address, name='address_insert'),

  path('update_increase/<int:pk>', views.plus_cart, name='update_increase'),
  path('update_decrease/<int:pk>', views.minus_cart, name='update_decrease'),
  
  path('mobile', views.mobiles, name='mobile'),
  path('electronics', views.electronics, name='electronics'),
  path('fashion', views.fashion_items, name='fashion'),
  path('laptop', views.laptops, name='laptop'),
  path('fashion-card', views.fashion_items, name='fashion-card'),
  path('product_view/<int:pk>', views.product_view, name='product_view'),
  path('product/<int:pk>', views.product_view, name = 'product'),
  
  path('registration', views.register, name='registration'),
  path('log_customer', views.loggin, name='log_customer'),
  path('logouut', views.logout, name='logouut'),
  
  
  path('admin_home', views.admin_home, name='admin_home'),
  path('customer_page', views.customer, name='customer_page'),
  path('category_page', views.category, name='category_page'),
  path('product_page', views.product, name='product_page'),
  # path('add_category', views.add_category, name='add_category'),
  path('insert_category', views.insert_category, name='insert_category'),
  # path('view_category', views.cat_viw, name='view_category'),
  path('order_page', views.order_page, name='order_page'),
  # path('order_view', views.order_viws, name='order_view'),

  path('update_order/<int:pk>', views.update, name='update_order'),
  path('order_update/<int:pk>', views.update_status, name='order_update'),
  
  path('add_product', views.add_product, name='add_product'),
  path('insert_product', views.insert_product, name='insert_product'),
  path('view_product', views.prod_viw, name='view_product'),
  path('admin_view_product/<int:pk>', views.admin_product_view, name='admin_view_product'),
  path('update_product/<int:pk>', views.update_prod, name='update_product'),
  path('product_updation/<int:pk>', views.product_update, name='product_updation'),
  
  # path('customer_view', views.customer_viw, name='customer_view'),
  # path('show_customer', views.show_cust, name='show_customer'),
  
  path('Show_product', views.show_prod, name='Show_product'),
 
  
  path('delete_customer/<int:pk>', views.delete_customer, name='delete_customer'),
  path('delete_product/<int:pk>', views.delete_product, name='delete_product'),
  
  path('search/',views.search, name='search'),
  
]