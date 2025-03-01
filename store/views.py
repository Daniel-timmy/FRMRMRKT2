from django.http import JsonResponse
from .models import * 
import json
import datetime
from .utils import cookieCart, cartData, guestOrder, send_email_to_product_owner
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from django.core.cache import cache

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
							name=first_name +" " + last_name,
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
	orders = Order.objects.filter(customer=request.user.customer).order_by('-date_ordered').all()[:5]
	context = {'orders':orders}
	print(orders)
	return render(request, 'business/profile.html', context)

@login_required(login_url='/login/')
def dashboard(request):
	if request.user.customer.acct_type != 'business':
		return redirect('/profile/')
	order_items = OrderItem.objects.filter(business=request.user.customer, order__complete=True).all()
	new_order =       	order_items.filter(status='New', order__complete=True).count()
	shipped_orders =  	order_items.filter(status='Shipped').order_by('-date_added')[:5]
	delivered_orders =	order_items.filter(status='Delivered').order_by('-date_added')[:5]
	pending_orders =  	order_items.filter(status='Pending').order_by('-date_added')[:5]

	cache_key = f"products_{request.user.customer.id}"

	aproducts = cache.get(cache_key)
	if not aproducts:
		aproducts = Product.objects.filter(owner=request.user.customer).all()
		cache.set(cache_key, aproducts, timeout=60*15)
	total_products = len(aproducts)

	products = aproducts.filter(owner=request.user.customer).order_by('-date_added')[:10]
	
	total_orders =          len(order_items)
	no_shipped_orders =  	order_items.filter(status='Shipped').count()
	no_delivered_orders =	order_items.filter(status='Delivered').count()
	no_pending_orders =  	order_items.filter(status='Pending').count()

	
	context = {'products': list(products), 'order_items': list(order_items), 
			'total_products': total_products, 'new_orders':new_order, 'shipped_orders': shipped_orders,
			'delivered_orders': delivered_orders, 'pending_orders': pending_orders, "total_orders": total_orders, "no_pending_orders": no_pending_orders,
			    "no_shipped_orders":no_shipped_orders, 'no_delivered_orders': no_delivered_orders}
	return render(request, 'business/dashboard.html', context)

def business_profile(request, id):
	owner = Customer.objects.get(id=id)

	aproducts = Product.objects.filter(owner=owner).all()
	total_products = len(aproducts)

	products = aproducts.filter(owner=owner).order_by('-date_added')[:10]

	
	context = {'products': list(products), 
			'total_products': total_products, 'customer': owner}
	print(context)
	return render(request, 'business/business_profile.html', context)


def store(request):

	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	categories = {'seeds': 'Seeds', 'vegetable': 'Vegetables', 'dairy': 'Dairy', 
			   'meat': 'Meat', 'tuber': 'Tuber', 'oil': 'Oil','herbs': 'Herbs and Spices',
			   'chicken': 'Chicken', 'fruits': 'Fruits'}
	context['categories'] = categories
	businesses = Customer.objects.filter(acct_type='business')
	context['businesses'] = businesses
	return render(request, 'store/store.html', context)

def reload_products(request):
	filter_data = json.loads(request.body)
	data = {}
	
	if len(filter_data['product_type']) > 0 and len(filter_data['business']) > 0:
		products = Product.objects.filter(category__in=filter_data['product_type'], owner__in=[int(x) for x in filter_data['business']] )
		data["products"] = list(products.values("id", "name", "price", "quantity", "owner", "rating", "image"))
		print(products)
	elif len(filter_data['product_type']) > 0:
		products = Product.objects.filter(category__in=filter_data['product_type'])
		data["products"] = list(products.values("id", "name", "price", "quantity", "owner", "rating", "image"))
	elif len(filter_data['business']) > 0:
		products = Product.objects.filter(owner__in=[int(x) for x in filter_data['business']])
		data["products"] = list(products.values("id", "name", "price", "quantity", "owner", "rating", "image"))
	else:
		products = Product.objects.all()
		data["products"] = list(products.values("id", "name", "price", "quantity", "owner", "rating", "image"))
	return JsonResponse(data)

@login_required(login_url='/login/')
def view_order(request, id):
	
	order = Order.objects.get(id=id)
	order_items = order.order_item_list
	context = {'orderItems': order_items}
	try:
		shippingAddress = ShippingAddress.objects.get(order=order)
	except Exception as e:
		print('Does not exist')
		shippingAddress = 'Not Available'

	context['shippingAddress'] = shippingAddress
	print(context)
	return render(request, 'business/view_order.html', context)


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

	orderItem, created = OrderItem.objects.get_or_create(order=order,
													   product=product, price=product.price, 
													   business=product.owner)


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
		
		# if order.shipping == True:
	shipping, created = ShippingAddress.objects.get_or_create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],)
			
	items = cartData(request)['items']

	product_detail_to_send = {}

	for item in items:
		product = Product.objects.get(id=item.product.id)
		product.quantity -= item.quantity
		product.save()
		product_detail_to_send.setdefault(product.owner.email, []).append(item)
	
	send_email_to_product_owner(product_detail_to_send, shipping)

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
		category = request.POST.get('product_category')
		# image = request.POST.get('product_image')

		product = Product(name=name, 
					price=price,
					quantity=quantity, 
					description=desc,
					owner=request.user.customer,
					category=category)
		product.save()
		messages.info(request, 'Product uploaded successfully')
	return render(request, 'business/upload.html')

@login_required(login_url='/login/')
def product_desc(request, id):
	product = Product.objects.get(id=id)
	data = cartData(request)
	cartItems = data['cartItems']
	context = {'product':product, 'cartItems':cartItems, 'reviews': product.get_reviews}
	print(context)
	return render(request, 'store/product_desc.html', context)

@login_required(login_url='/login/')
def update_product(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		if data['action'] == 'update':
			product = Product.objects.get(id=data['productId'])
			updates = data['productData']
			for key, value in updates.items():
				if key == 'price':
					setattr(product, key, float(value))
				elif key == 'quantity':
					setattr(product, key, int(value))
				else:
					setattr(product, key, value)
			product.save()
		elif data['action'] == 'delete':
			product = Product.objects.get(id=data['productId'])
			print(product)
			product.delete()
		return JsonResponse('Product updated', safe=False)
	return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required(login_url='/login/')
def update_customer(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		if data['action'] == 'update':
			customer = Customer.objects.get(id=data['customerId'])
			updates = data['customerData']
			for key, value in updates.items():
				setattr(customer, key, value)
			customer.save()
		elif data['action'] == 'delete':
			customer = Customer.objects.get(id=data['productId'])
			print(customer)
			customer.delete()
		return JsonResponse('Customer details updated', safe=False)
	return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required(login_url='/login/')
def update_order_item(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		if data['action'] == 'update':
			order_item = OrderItem.objects.get(id=data['orderItemId'])
			updates = data['OrderItemData']
			for key, value in updates.items():
				setattr(order_item, key, value)
			order_item.save()
		elif data['action'] == 'delete':
			order_item = OrderItem.objects.get(id=data['orderItemId'])
			order_item.delete()
		return JsonResponse('Order updated', safe=False)
	return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required(login_url='/login/')
def show_all(request, status):
	if request.user.customer.acct_type != 'business':
		return redirect('/profile/')
	order_item_map = {'pending': 'Pending', 'shipped': 'Shipped', 'delivered': 'Delivered', 'new_orders': 'New'}
	
	if status == 'purchases':
		orders = Order.objects.filter(customer=request.user.customer).order_by('-date_ordered').all()
		items = []
		for order in orders:
			items = items + list(order.order_item_list)
	
	elif status == 'products':
		cache_key = f"products_{request.user.customer.id}"
		items = cache.get(cache_key)
		if not items:
			items = Product.objects.filter(owner=request.user.customer).all()
			cache.set(cache_key, items, timeout=60*15)  # Cache for 15 minutes

	
	elif status in order_item_map:
		order_items = OrderItem.objects.filter(business=request.user.customer).all()
		items =  order_items.filter(status=order_item_map[status]).order_by('-date_added')
		if status == 'new_orders':
			c_items = []
			for item in items:
				if item.order.complete == True:
					item.status = 'Pending'
					item.save()
					c_items.append(item)


	context = {'items': c_items, 'status': status}
	
	print(context)
	return render(request, 'business/show_all.html', context)


@login_required(login_url='/login/')
def review(request, id):
	if request.method == 'POST':
		data = json.loads(request.body)
		print(data)
		product = Product.objects.get(id=id)
		review = Reviews.objects.create(customer=request.user.customer, 
								  product=product, review=data['review'], 
								  rating=int(data['rating']) if data['rating'] != '' else 0)
		review.save()
		print(Reviews.objects.all())
		print(product.get_rating)
		return JsonResponse('Review submitted', safe=False)
	return JsonResponse({'error': 'Invalid request method'}, status=400)