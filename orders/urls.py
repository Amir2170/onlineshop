from django.urls import path

from . import views


app_name = 'orders'
urlpatterns=[
	path('create/', views.order_create, name='create'),
	path('<int:order_id>/', views.detail, name='detail'),
	path('coupon/<int:order_id>/', views.coupon_apply, name='coupon_apply'),
#	path('payment/<int:order_id>/<int:price>/', views.payment, name='payment'),
#	path('verify/', views.verify, name='verify'),
]