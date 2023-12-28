from django.contrib import admin
from .models import Cart, Tax
# Register your models here.

class CardAdmin(admin.ModelAdmin):
    list_display = ('user', 'fooditem', 'quantity', 'updated_at')

class TaxAdmin(admin.ModelAdmin):
    list_display = ('tax_type', 'tax_percentage', 'is_active')

admin.site.register(Cart, CardAdmin)
admin.site.register(Tax, TaxAdmin)
