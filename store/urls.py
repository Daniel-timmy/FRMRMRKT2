from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
    path('store/', views.store, name="store"),
    path('store/undefined', views.store, name="store"),

	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('upload_product/', views.upload_product, name="upload_product"),
    path('login/',views.log_in, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.log_out, name="logout"),
    path('profile/', views.profile, name="profile"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('product_desc/<int:id>/', views.product_desc, name="product_desc"),
    path('update_product/', views.update_product, name="update_product"),
    path('update_customer/', views.update_customer, name="update_customer"),
    path('show_all/<str:status>/', views.show_all, name="show_all"),
    path('update_order_item/', views.update_order_item, name="update_order_item"),
    path('review/<int:id>/', views.review, name="review"),
    path('reload_products/', views.reload_products, name="reload_products"),
    path('business_profile/<int:id>/', views.business_profile, name="business_profile"),
]