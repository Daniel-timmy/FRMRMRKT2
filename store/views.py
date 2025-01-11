from django.http import JsonResponse
from .models import * 
import json
import datetime
from .utils import cookieCart, cartData, guestOrder
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *


def home(request):
    return render(request, 'home.html')

# Define a view function for the login page
def log_in(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not User.objects.filter(username=email).exists():
            messages.error(request, 'Incorrect email')
            return redirect('/login/')
        
        user = authenticate(username=email, password=password)
        
        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/store/')
    
    return render(request, 'store/login.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        acct_type = request.POST.get('acct_type')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.info(request, 'Password does not match Confirm Password.'
						  )
            return redirect('/register/')
        
        user = User.objects.filter(username=email)
        
        if user.exists():
            messages.info(request, "User with email already exist!")
            return redirect('/register/')
        
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=email
        )
        
        user.set_password(password)
        user.save()
        customer = Customer(user=user,
							name=first_name + last_name,
							email=email,
							acct_type=acct_type)
        customer.save()
        
        messages.info(request, "Account created Successfully!")
        login(request, user)
        return redirect('/store/')
    
    return render(request, 'store/register.html')


def log_out(request):
	logout(request)
	return redirect('/store/')


@login_required(login_url='/login/')
def profile(request):

	return render(request, 'business/profile.html')

@login_required(login_url='/login/')
def dashboard(request):
	if request.user.customer.acct_type != 'business':
		return redirect('/profile/')
	return render(request, 'business/dashboard.html')


def store(request):

	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def cart(request):

	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	print(items)
		
	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		if product.quantity > orderItem.quantity:
			orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

		total = float(data['form']['total'])
		order.transaction_id = transaction_id

		if total == order.get_cart_total:
			order.complete = True
		order.save()
		
		if order.shipping == True:
			ShippingAddress.objects.create(
				customer=customer,
				order=order,
				address=data['shipping']['address'],
				city=data['shipping']['city'],
				state=data['shipping']['state'],
				zipcode=data['shipping']['zipcode'],)
			
	items = cartData(request)['items']

	for item in items:
		product = Product.objects.get(id=item.product.id)
		product.quantity -= item.quantity
		product.save()

	# send email to the product owner
	return JsonResponse('Payment submitted..', safe=False)

@login_required(login_url='/login/')
def upload_product(request):
	if request.method == "POST":
		if request.user.customer.acct_type != 'business':
			messages.error(request, 'You are not authorized to upload product')
			return redirect('/store/')
		name = request.POST.get('product_name')
		price = request.POST.get('price') 
		quantity = request.POST.get('quantity')
		desc = request.POST.get('desc')
		# image = request.POST.get('product_image')

		product = Product(name=name, 
					price=price,
					quantity=quantity, 
					description=desc,
					owner=request.user.customer)
		product.save()
		messages.info(request, 'Product uploaded successfully')
	return render(request, 'business/upload.html')

@login_required(login_url='/login/')
def product_desc(request, id):
	product = Product.objects.get(id=id)
	data = cartData(request)
	cartItems = data['cartItems']

	context = {'product':product, 'cartItems':cartItems}
	return render(request, 'store/product_desc.html', context)
