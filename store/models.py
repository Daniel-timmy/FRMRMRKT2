from django.db import models

from django.contrib.auth.models import User
from datetime import datetime


class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)
	acct_type = models.CharField(max_length=25, default='regular')
	business_description = models.TextField(null=True)
	business_location = models.CharField(max_length=30, default='Lagos, Nigeria')
	# pic = models.ImageField()
	# background = models.ImageField()

	def __str__(self):
		return self.email



class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    quantity = models.IntegerField(default=10)
    digital = models.BooleanField(default=False,null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    # category = models.CharField(null=True)
    date_added = models.DateTimeField(default=datetime.now())

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    def __str__(self):
        return self.name
	
class Reviews(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	product = models.ForeignKey(Product, null=False, on_delete=models.CASCADE)
	review = models.TextField(blank=False)
	#pics = models.Image
	created_at = models.DateTimeField(auto_now_add=True)
		

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
	
	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total
	
	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total
	
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping
	@property
	def order_item_list(self):
		return self.orderitem_set.all()

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	price = models.FloatField(null=False, default=0)
	business = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	status = models.CharField(default='New', null=True, max_length=20)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total
	def __str__(self):
		return f'name: {self.product.name}, quantity: {self.quantity}'
	
class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address