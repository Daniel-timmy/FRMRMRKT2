import json
from .models import *
from django.core.mail import send_mail
from django.conf import settings

def cookieCart(request):

	#Create empty cart for now for non-logged in user
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}
		print('CART:', cart)

	items = []
	order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
	cartItems = order['get_cart_items']

	for i in cart:
		#We use try block to prevent items in cart that may have been removed from causing error
		try:
			cartItems += cart[i]['quantity']

			product = Product.objects.get(id=i)
			total = (product.price * cart[i]['quantity'])

			order['get_cart_total'] += total
			order['get_cart_items'] += cart[i]['quantity']

			item = {
				'id':product.id,
				'product':{'id':product.id,'name':product.name, 'price':product.price, 
				'imageURL':product.imageURL}, 'quantity':cart[i]['quantity'],
				'digital':product.digital,'get_total':total, 
				'available_quantity': product.quantity,
				}
			items.append(item)

			if product.digital == False:
				order['shipping'] = True
		except:
			pass
			
	return {'cartItems':cartItems ,'order':order, 'items':items}

def send_email_to_product_owner(product_detail_to_send, shipping):
	# send email to the product owner


	shipping_info = f"""
		+---------------------+--------------------------------+
		| Field               | Value                          |
		+---------------------+--------------------------------+
		| Customer            | {shipping.customer.email}      |
		| Order               | {shipping.order.transaction_id}      |
		| Address             | {shipping.address}  		   |
		| City                | {shipping.city}				   |
		| State               | {shipping.state}    		   |
		| Zipcode             | {shipping.zipcode}			   |
		+---------------------+--------------------------------+
		"""
	for key in product_detail_to_send.keys():
		product = []
		for item in product_detail_to_send[key]:
			formatted_string = f"""
				Product order info
				+---------------------+--------------------------------+
				| Field               | Value                          |
				+---------------------+--------------------------------+
				| Product ID          | {item.product.id}	           |
				| Product Name        | {item.product.name}    		   |
				| Product Price       | {item.product.price}   		   |
				| Quantity            | {item.quantity}                |
				| Total               | {item.get_total}               |
				| Available Quantity  | {item.product.quantity}      |
				+---------------------+--------------------------------+

				"""
			product.append(formatted_string)
		product.append(shipping_info)
		email_address = key
		message = ''.join(product)
		subject = f'Product Order: {shipping.order.transaction_id}'
		context = {}
		print(f"""
				'Product owner':{email_address}
				{subject}
				{message}
		""")
		# try:
		# 	send_mail(subject, message, 
		# 	 settings.EMAIL_HOST_USER, [email_address])
		# except Exception as e:
		# 	context['result'] = 'Email sent successfully'
		# else:
		# 	context['result'] = 'All fields are required'
		

def cartData(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		cookieData = cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']

	return {'cartItems':cartItems ,'order':order, 'items':items}

def guestOrder(request, data):
	name = data['form']['name']
	email = data['form']['email']

	cookieData = cookieCart(request)
	items = cookieData['items']

	customer, created = Customer.objects.get_or_create(
			email=email,
			)
	customer.name = name
	customer.save()

	order = Order.objects.create(
		customer=customer,
		complete=False,
		)

	for item in items:
		product = Product.objects.get(id=item['id'])
		# orderItem = OrderItem.objects.create(
		# 	product=product,
		# 	order=order,
		# 	quantity=item['quantity'],
		# )
		orderItem = OrderItem.objects.create(
			product=product,
			order=order,
			quantity=item['quantity'],
			business=product.owner,
			price=product.price,
		)
	return customer, order