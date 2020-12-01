from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
	
	def create_user(self, email, name, password):
		if not email:
			raise ValueError('User must have an Email')
		
		if not name:
			raise ValueError('User must have a name')
		
		user = self.model(
			email=self.normalize_email(email),
			name=name,
		)
		user.set_password(password)
		user.save(using=self._db)
		return user
	
	def create_superuser(self, email, name, password):
		user = self.create_user(email, name, password)
		user.is_admin = True
		user.save(using=self._db)
		return user
