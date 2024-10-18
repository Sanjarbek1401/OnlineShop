from django.contrib import admin
from .models import Category, Product, Comment

admin.site.register(Comment)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price','discount', 'available', 'rating', 'created', 'updated')
    search_fields = ('name',)
    list_filter = ('available', 'created', 'updated')
    list_editable = ('available', 'price', 'discount','rating')
    prepopulated_fields = {"slug": ("name",)}
