from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from . models import *
import random
import string
import re

# Create your views here.


# user views
def home(request):  
  pro_mobile = Category.objects.get(category_name = 'mobile')
  mobiles = Product.objects.filter(prdt_category = pro_mobile)
  
  pro_laptop = Category.objects.get(category_name = 'laptop')
  laptops = Product.objects.filter(prdt_category = pro_laptop)
  
  pro_electronics = Category.objects.get(category_name = 'electronics')
  electro = Product.objects.filter(prdt_category = pro_electronics)
  
  all = Product.objects.all()
    
  context = {
    'mobile':mobiles,
    'laptop':laptops,
    'electronics':electro,
    'all':all,

    }
  return render(request, 'home.html', context)




def signin(request):
  return render(request, 'signin.html')




def generate_password(length=8):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def register(request):
  if request.method == 'POST':
    
    generated_password = generate_password()
    
    fname = request.POST['f_name']
    lname = request.POST['l_name']
    mobile = request.POST['mobile']
    address = request.POST['address']
    locality = request.POST['locality']
    city = request.POST['city']
    state = request.POST['state']
    pincode = request.POST['pincode']
    uname = request.POST['user_name']
    email = request.POST['email']
    passw = generated_password
    # cpassw = request.POST['cpassword']
    # if passw == cpassw:
      # pattern = r"[^\w\s]"  # Matches any character that is not alphanumeric or whitespace
      # check_special_char = re.search(pattern, passw)
      # if not check_special_char:
      #   messages.info(request, 'Sorry, password must include a special character...')
      #   return redirect('register')
      # length_of_pass = len(passw)
      # if not 8 <= length_of_pass <= 26:
      #   messages.info(request, 'Sorry, password must include 8 - 26 character...')
      #   return redirect('register') 
      # uppercase_characters = set([c for c in passw if c.isupper()])
      # if not len(uppercase_characters) > 0:
      #   messages.info(request, 'Sorry, password must include Atleast One Uppercase character...')
      #   return redirect('register')  
      # digit_characters = set([c for c in passw if c.isdigit()])
      # if not len(digit_characters) > 0:  
      #   messages.info(request, 'Sorry, password must include Atleast One digit...')
      #   return redirect('register')
    if User.objects.filter(username = uname).exists():
      messages.info(request, 'Sorry, Username already exists')
      return redirect('register')
    elif Customer.objects.filter(cust_mobile = mobile).exists():
      messages.info(request, 'Sorry Mobile number already exists')
      return redirect('register')
    elif not User.objects.filter(email = email).exists():
      
      user = User.objects.create_user(first_name = fname,
                              last_name = lname,
                              username = uname,
                              email = email,
                              password = passw)
      user.save()
    
      data = User.objects.get(id = user.id)
      cus_data = Customer(cust_mobile = mobile,
                          cust_address = address,
                          cust_locality = locality,
                          cust_city = city,
                          cust_state = state,
                          cust_pincode = pincode,
                          cust_user = data)
      cus_data.save()
      
      subject = 'Welcome to Shopper Cart'
      message = 'Greetings' +data.first_name +' '+data.last_name+',\nWe  Thank you for your interest in Shopper cart.\nHere is your username and password:\nUsername:'+ user.username+'\nPassword: '+ generated_password +'\nKeep it secure.' 
      recipient = request.POST['email']     #  recipient =request.POST["inputTagName"]
      send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])
      messages.success(request, 'Welcome '+ data.first_name +' '+ data.last_name +' '+'you have successfully registered. Please login..!')
      print(passw)
      return redirect('login')
      # else:
      #   messages.info(request, 'Sorry, Email already exists')
      #   return redirect('register')
    else:
      messages.info(request, 'Sorry, Email already exists')
      return redirect('register')
    # else:
      # user = User.objects.create_user(first_name = fname,
      #                                 last_name = lname,
      #                                 username = uname,
      #                                 email = email,
      #                                 password = passw)
      # user.save()
      
      # data = User.objects.get(id = user.id)
      # cus_data = Customer(cust_mobile = mobile,
      #                     cust_address = address,
      #                     cust_locality = locality,
      #                     cust_city = city,
      #                     cust_state = state,
      #                     cust_pincode = pincode,
      #                     cust_user = data)
      # cus_data.save()
      # messages.success(request, 'Welcome '+ data.first_name +' '+ data.last_name +' '+'you have successfully registered. Please login..!')
      # return redirect('login') 
         
    # else:
    #   messages.info(request, 'Sorry, password and confirm password does not match')
    #   return redirect('register')





def signup(request):
  return render(request, 'signup.html')

def loggin(request):
  if request.method == 'POST':
    uname = request.POST['log_user']
    passwo = request.POST['log_pass']
    user = auth.authenticate(username = uname,
                             password = passwo)
    if user is not None:
      if user.is_staff:
        login (request, user)
        return redirect('admin_home')
      else:
        auth.login(request, user)
        return redirect('/')
    else:
      messages.info(request, 'Sorry, Username or Password seems to be incorrect. If not registered yet, Please register')
      return redirect('login')
    
    
    
@login_required(login_url='login')
def change_pass(request):
  return render(request, 'change_password.html')

def pass_change(request):
  if request.method == 'POST':
    current_pass = request.POST.get('current_pass')
    new_pass = request.POST['password']
    repeat_pass = request.POST['cpassword']
    user = authenticate(username = request.user.username, password = current_pass)

    if new_pass == repeat_pass:
      if user is not None:
        user.set_password(new_pass)
        user.save()
        messages.success(request, 'Password changed successfully')
        return redirect('change_pass')
      else:
        messages.info(request, 'Sorry Current password is Invalid, Please try again')
        return redirect('change_pass')
    else:
      messages.info(request, 'Password and repeat Password doesnot match')
      return redirect('change_pass')
      
    


def view_profile(request):
  user = request.user
  profile = Customer.objects.filter(cust_user = user.id)  #cust_user => foreignkey user
  return render(request, 'view_user_profile.html', {'profile':profile})

def profile(request, pk):
  if request.method == 'POST':
    update = Customer.objects.get(id = pk)
    fname = request.POST['u_fname']
    lname = request.POST['u_lname']
    email = request.POST['u_email']
    update.cust_mobile = request.POST.get('u_mobile')
    update.cust_address = request.POST.get('u_address')
    update.cust_locality = request.POST.get('u_locality')
    update.cust_city = request.POST.get('u_city')
    update.cust_state = request.POST.get('u_state')
    update.cust_pincode = request.POST.get('u_pincode')
    
    update.save()
    
    user = request.user
    user.first_name = fname
    user.last_name = lname
    user.email = email
    
    user.save()
    return redirect('profile')
  
  
  
  
  

def mobiles(request):
  pro_mobile = Category.objects.get(category_name = 'mobile')
  mob = Product.objects.filter(prdt_category = pro_mobile)
  return render(request, 'mobile.html', {'mobile':mob})

def electronics(request):
  pro_electronics = Category.objects.get(category_name = 'electronics')
  electro = Product.objects.filter(prdt_category = pro_electronics)
  return render(request, 'electronics.html', {'electronics':electro})

def fashion_items(request):
  pro_fashion_tp = Category.objects.get(category_name = 'topwears')
  topwears = Product.objects.filter(prdt_category = pro_fashion_tp)
  
  pro_fashion_watch = Category.objects.get(category_name = 'watch')
  watches = Product.objects.filter(prdt_category = pro_fashion_watch)
  
  pro_fashion_bw = Category.objects.get(category_name = 'bottomwears')
  bottomwears = Product.objects.filter(prdt_category = pro_fashion_bw)
  
  pro_fashion_shoes = Category.objects.get(category_name = 'shoes')
  shoes = Product.objects.filter(prdt_category = pro_fashion_shoes)
  
  context = {
    'topwear':topwears,
    'watch':watches,
    'bottomwear':bottomwears,
    'shoe':shoes
  }
  return render(request, 'fashion.html', context)

def laptops(request):
  pro_laptop = Category.objects.get(category_name = 'laptop')
  laptops = Product.objects.filter(prdt_category = pro_laptop)
  return render(request, 'laptop.html', {'laptop':laptops})




def product_view(request, pk):
    product = Product.objects.get(id = pk)
    return render(request, 'product_details.html', {'product':product})
  
def admin_product_view(request, pk):
    product = Product.objects.get(id = pk)
    return render(request, 'admin_product_view.html', {'product':product})




  
@login_required(login_url='login')
def show_cart(request):
  if request.user.is_authenticated:
      user = request.user
      cart = Cart.objects.filter(user=user)
      amount = 0.0
      shipping_amount = 70.0
      total_amount = 0.0
      cart_product = [p for p in Cart.objects.all() if p.user == user]
      
      if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.prdt_discounted_price)
            amount += tempamount
            total_amount = amount + shipping_amount
        return render(request, 'add_to_cart.html', {'carts':cart, 'totalamount':total_amount, 'amount':amount})
      else:
          return render(request, 'empty_cart.html')  
        
       
@login_required(login_url='login') 
def add_cart(request):
  if request.user.is_authenticated:
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id = product_id)
    
    if Cart.objects.filter(product = product, user = user).exists():
      cart_item = Cart.objects.get(product=product, user=user)
      cart_item.quantity += 1
      cart_item.save()
      return redirect('cart')
    else:
    
      cart = Cart.objects.create(user = user,
                                product = product)
      cart.save()
      print('hi')
      return redirect('cart')
  
@login_required(login_url='login')  
def plus_cart(request, pk):
  pro_inc = Cart.objects.get(id = pk)
  pro_inc.quantity +=1
  pro_inc.save()
  return redirect('cart')
  
@login_required(login_url='login')
def minus_cart(request, pk):
  pro_dec = Cart.objects.get(id = pk)
  if pro_dec.quantity > 1:
    pro_dec.quantity -= 1
    pro_dec.save()
    return redirect('cart')
  else:
    return redirect('cart')

  
  
  
@login_required(login_url='login')
def remove_cart(request, pk):
  product = Cart.objects.get(id = pk)
  product.delete()
  return redirect('cart')


@login_required(login_url='login')
def buy_now(request, pk):
  add = Customer.objects.get(cust_user = request.user)
  product = Product.objects.get(id = pk)
  shipping_amount = 70.0
  totalamount = shipping_amount + product.prdt_discounted_price
  return render(request, 'buy_now.html', {'add':add, 'product':product, 'totalamount':totalamount})
  
  
@login_required(login_url='login')  
def checkout(request):
    user = request.user
    add = Customer.objects.filter(cust_user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.prdt_discounted_price)
            amount += tempamount
            totalamount = amount + shipping_amount
    return render(request,'checkout.html',{'add':add, 'totalamount':totalamount, 'cart_items':cart_items})
  

# def address(request):
#   return render(request, 'address.html')

# def insert_address(request):
#   if request.method == 'POST':
#     user = request.user
    
#     ad_first = request.POST['ad_f_name']
#     ad_last = request.POST['ad_l_name']
#     ad_address = request.POST['add_address']
#     ad_locality = request.POST['add_locality']
#     ad_city = request.POST['add_city']
#     ad_state = request.POST['add_state']
#     ad_pin = request.POST['add_pincode']
#     ad_mobile = request.POST['add_mobile']
#     user = User.objects.create_user(first_name = ad_first,
#                                     last_name = ad_last)
#     user.save()
    
#     data = User.objects.get(id = user.id)
#     cus = Customer( cust_user = data,
#                 cust_address = ad_address,
#                 cust_locality = ad_locality,
#                 cust_city = ad_city,
#                 cust_state = ad_state,
#                 cust_pincode = ad_pin,
#                 cust_mobile = ad_mobile)
#     cus.save()
#     messages.success(request, 'Successfully added')
#     return redirect('add_address')
#   else:
#     messages.success(request, 'Please try again')
#     return redirect('add_address')



@login_required(login_url='login')
def orders(request):
  op = OrderPlaced.objects.filter(user = request.user)
  return render(request, 'order.html', {'order_placed':op})

def ordered(request):
  user = request.user
  custid = request.GET.get('customid')
  customer = Customer.objects.get(id = custid)
  cart = Cart.objects.filter(user = user)
  
  for c in cart:
    orders = OrderPlaced(user = user,
                customer = customer,
                product = c.product,
                quantity = c.quantity)
    orders.save()
    c.delete()
    return redirect('order')
  
def buy_order(request, pk):
    user = request.user
    customer = Customer.objects.get(cust_user = request.user)
    prod = Product.objects.get(id = pk)

    orders = OrderPlaced(user = user,
                customer = customer,
                product = prod,
                quantity = 1)
    orders.save()
    return redirect('order')
    
    
            
        
def logout(request):
  auth.logout(request)
  return redirect('/')   




# admin views
def admin_home(request):
  return render(request, 'admin_home.html')

def customer(request):
  cus = Customer.objects.all()
  return render(request, 'customer_page.html', {'show_customer':cus})

def category(request):
  cat = Category.objects.all()
  return render(request, 'category_page.html', {'category':cat})

# def add_category(request):
#   return render(request, 'add_category.html')

def insert_category(request):
  if request.method == 'POST':
    add_cate = request.POST['insrt_cate']
    if Category.objects.filter(category_name = add_cate).exists():
      messages.info(request, 'Sorry, Category already exists')
      return redirect('category_page')
    else:
      inserting = Category(category_name = add_cate)
      inserting.save()
      messages.success(request, 'Successfully inserted'+' '+add_cate)
      return redirect('category_page')
    
    
    

def product(request):
  return render(request, 'product_page.html')

def prod_viw(request):
  prod = Product.objects.all()
  return render(request, 'view_product.html' ,{'product':prod})

def add_product(request):
  catega = Category.objects.all()
  return render(request, 'add_product.html', {'catagory':catega})
  
def insert_product(request):
  if request.method == 'POST':
    brand = request.POST['p_brand']
    title = request.POST['p_title']
    desc = request.POST['p_description']
    sell = request.POST['p_selling']
    discount = request.POST['p_discounted']
    
    select = request.POST['p_category']
    categ = Category.objects.get(id = select)
    
    img = request.FILES.get('p_image')
    product = Product(prdt_brand = brand,
                      prdt_title = title,
                      prdt_description = desc,
                      prdt_selling_price = sell,
                      prdt_discounted_price = discount,
                      prdt_category = categ,
                      prdt_image = img)
    product.save()
    messages.success(request, 'Successfully inserted')
    return redirect('add_product')
  
def show_prod(request):
  pro = Product.objects.all()
  return render(request, 'show_product.html', {'show_product':pro})

def update_prod(request, pk):
  prod = Product.objects.get(id = pk)
  cat = Category.objects.all()
  return render(request, 'update_product.html', {'product':prod, 'catagory':cat})

def product_update(request, pk):
  if request.method == 'POST':
    update = Product.objects.get(id = pk)
    update.prdt_brand = request.POST.get('up_brand')
    update.prdt_title = request.POST.get('up_title')
    update.prdt_description = request.POST.get('up_description')
    update.prdt_selling_price = request.POST.get('up_selling')
    update.prdt_discounted_price = request.POST.get('up_discounted')
    
    category = request.POST.get('up_category')
    update.prdt_category = Category.objects.get( id = category )

    old = update.prdt_image
    new = request.FILES.get('up_image')
    
    if old != None and new == None:
      update.prdt_image = old
    else:
      update.prdt_image = new
    
    update.save()
    return redirect('view_product')
    




# def customer_viw(request):
#   cust = Customer.objects.all()
#   return render(request, 'admin_customer_view.html', {'customer':cust})

# def cat_viw(request):
#   cat = Category.objects.all()
#   return render(request, 'admin_category_view.html', {'category':cat})

# def show_cust(request):
#   cus = Customer.objects.all()
#   return render(request, 'show_customer.html', {'show_customer':cus})


def order_page(request):
  op = OrderPlaced.objects.all()
  return render(request, 'order_page.html', {'order':op})

# def order_viws(request):
#   op = OrderPlaced.objects.all()
#   return render(request, 'order_view.html', {'order':op})





def update(request, pk):
  order = OrderPlaced.objects.get(id = pk)
  return render(request, 'update_status.html' ,{'orders':order})


def update_status(request, pk):
  update = OrderPlaced.objects.get(id = pk)
  update.status = request.GET.get('status')
  update.save()
  return redirect('order_page')





def delete_product(request, pk):
  product = Product.objects.get(id = pk)
  product.delete()
  return redirect('Show_product')

def delete_customer(request, pk):
  customer = Customer.objects.get(id = pk)
  user = customer.cust_user
  
  customer.delete()
  user.delete()
  return redirect('customer_page')

def search(request):
    if 'q' in request.GET:
        query = request.GET['q']
        if query:
            matching_products = Product.objects.filter(prdt_brand__istartswith=query)
        else:
            matching_products = Product.objects.none()
            messages.info(request,'Sorry, no search result found!')
    else:
        matching_products = Product.objects.none()
        messages.info(request,'Sorry, no search result found!')

    return render(request, 'search.html', {'data': matching_products})