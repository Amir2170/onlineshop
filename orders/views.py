from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
#from suds.client import Client
#from django.http import HttpResponse

from .models import Order, OrderItem, Coupon
from cart.cart_session import Cart
from .forms import CouponForm

#MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
#client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
#description = ت"وضیحات مربوط به تراکنش را در این قسمت وارد کنید"
#email = request.user.email
#mobile = '09123456789'
#CallbackURL = 'http://localhost:8000/orders/verify/' #change in productio 


@login_required
def order_create(request):
	cart = Cart(request)
	order = Order.objects.create(user=request.user)
	for item in cart:
		OrderItem.objects.create(
			order=order, product=item['product'],
			price=item['price'], quantity=item['quantity'],
		)
	cart.clear()
	return redirect('orders:detail', order.id)


@login_required
def detail(request, order_id):
	order = get_object_or_404(Order, id=order_id)
	form = CouponForm()
	return render(request, 'orders/detail.html', {
		'order': order, 'form': form
		},)


@require_POST
def coupon_apply(request, order_id):
	now = timezone.now()
	form = CouponForm(request.POST)
	if form.is_valid():
		code = form.cleaned_data['code']
		try:
			coupon = Coupon.objects.get(
				code__iexact=code, valid_from__lte=now, 
				valid_to__gte=now, active=True,
			)
		except Coupon.DoesNotExist:
			messages.error(request, 'Coupon does not exists', 'danger')
			return redirect('orders:detail', order_id)
		order = Order.objects.get(id=order_id)
		order.discount = coupon.discount
		order.save()
		coupon.active = False
		coupon.save()
		return redirect('orders:detail', order_id)


#@login_required
#def payment(request, order_id, price):
#	global amount, g_order_id
#	g_order_id = order_id
#	amount = price
#   if result.Status == 100:
#    	return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
#   else:
#  	return HttpResponse('Error code: ' + str(result.Status))


#@login_required
#def verify(request):
#	if request.GET.get('Status') == 'OK':
# 	result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
#    	if result.Status == 100:
#			order = Order.objects.get(id=g_order_id)
#			order.price = True
#			order.save()
#			messages.success(request, 'Transaction was successful')
#			return.redirect('shop:home')
#    	elif result.Status == 101:
#        	return HttpResponse('Transaction submitted ')
#    	else:
#        	return HttpResponse('Transaction failed.\nStatus')
#	else:
#    	return HttpResponse('Transaction failed or canceled by user')








