from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model

from .forms import UserLoginForm, UserRegistrationForm

User = get_user_model()


def user_login(request):
	if request.method == 'POST':
		form = UserLoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(
				request, username=cd['email'], password=cd['password']
			)
			if user is not None:
				login(request, user)
				messages.success(request, 'You logged in successfully')
				return redirect('shop:home')
			else:
				messages.error(
					request, 
					'email or password is incorrect', 
					extra_tags='danger'
				)
	else:
		form = UserLoginForm
		
	return render(request, 'login.html', {'form': form})


def user_logout(request):
	logout(request)
	messages.success(request, 'You logged out successfully')
	return redirect('shop:home')
	

def user_register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = User.objects.create_user(email=cd['email'], 
				name=cd['name'], password=cd['password']
			)
			user.save()
			messages.success(request, 'You registered successfully')
			return redirect('shop:home')
	else:
		form = UserRegistrationForm()
		
	return render(request, 'register.html', {'form': form})
