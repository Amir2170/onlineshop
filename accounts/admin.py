from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .forms import UserChangeForm, UserCreationForm
from .models import User


class UserAdmin(BaseUserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm
	
	list_display = ('email', 'name', 'is_admin')
	list_filter = ('is_admin',)
	
	fieldsets=(
		(None, {'fields': ('email', 'password',)}),
		('Personal info', {'fields': ('name', 'is_active')}),
		('Permissions', {'fields': ('is_admin',)}),
	)
	add_fieldsets = (
		(None, {'fields': ('name', 'email', 'password1', 'password2')}),
	)
	search_fields = ('email',)
	ordering = ('email',)
	filter_horizontal = ()


admin.site.register(User, UserAdmin)

admin.site.unregister(Group)
