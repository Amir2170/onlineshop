from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User


class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label="password", 
		widget=forms.PasswordInput
	)
	password2 = forms.CharField(label="password confirmation",
		widget=forms.PasswordInput
	)
	
	class Meta:
		models = User
		fields = ('email', 'name')
		
	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise ValidationErr("Passwords don't match")
		return password2
	
	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user
	
	
class UserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField()
	
	class Meta:
		model = User
		fields = ('email', 'password', 'name')
	
	def clean_password(self):
		return self.initial['password']
		
		
class UserLoginForm(forms.Form):
	email = forms.EmailField(
		widget=forms.EmailInput(attrs={'class': 'form_control'}))
	password = forms.CharField(
		widget=forms.PasswordInput(attrs={'class': 'form_control'}))


class UserRegistrationForm(forms.Form):
	email = forms.EmailField(
		widget=forms.EmailInput(attrs={'class': 'form_control'}))
	password = forms.CharField(
		widget=forms.PasswordInput(attrs={'class': 'form_control'}))
	name = forms.CharField(
		widget=forms.TextInput(attrs={'class': 'form_control'}))

