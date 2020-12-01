from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .manager import MyUserManager


class User(AbstractBaseUser):
	email = models.CharField(max_length=100, unique=True)
	name = models.CharField(max_length=200)
	
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	
	objects = MyUserManager()
	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name',]
	
	def __str__(self):
		return self.email
		
	def has_perm(self, perm, object=None):
		return True
	
	def has_module_perms(self, app_label):
		return True
		
	@property
	def is_staff(self):
		return self.is_admin
