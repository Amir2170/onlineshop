from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext

from .models import Product, Category


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
	list_display = ('name', 'slug',)
	prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
	list_display = ('name', 'price', 'available',)
	list_filter = ('available', 'created',)
	list_editable = ('price', 'available',)
	prepopulated_fields = {'slug': ('name',)}
	raw_id_fields = ('category',)
	actions = ['make_available',]
	
	def make_available(self, request, queryset):
		available_now = queryset.update(available=True)
		self.message_user(request, ngettext(
			f'selected merchendise is available now',
			f'selected merchendises are available now',
			available_now
		), messages.SUCCESS)
	make_available.short_description =(
	'Make selected merchendise available'
)
