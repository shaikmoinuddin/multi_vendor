from django.contrib import admin
from .models import Category, FoodItem

# prepopulated in slugfield
class category(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ('category_name', 'vendor', 'updated_at')
    search_fields = ('category_name', 'vendor__vendor_name')


# prepopulated in slugfield
class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('food_title',)}
    list_display = ('food_title', 'category', 'vendor', 'price', 'is_available', 'updated_at')
    search_fields = ('food_title', 'category__category_name', 'vendor__vendor_name', 'price')
    list_filter = ('is_available',)

admin.site.register(Category, category)
admin.site.register(FoodItem, FoodItemAdmin)
