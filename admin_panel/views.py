from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from shop.models import Category, Product,UserProfile
from django import forms
from django.urls import reverse_lazy
from django.utils.text import slugify


class UserListView(ListView):
    model = UserProfile
    template_name = 'admin_panel/user_list.html'
    context_object_name = 'users'

class UserCreateView(CreateView):
    model = UserProfile
    template_name = 'admin_panel/user_form.html'
    fields = ['user', 'phone_number','address']
    success_url = reverse_lazy('admin_panel:user_list')


class UserUpdateView(UpdateView):
    model = UserProfile
    template_name = 'admin_panel/user_form.html'
    fields = ['user', 'phone_number','address']
    success_url = reverse_lazy('admin_panel:user_list')

class UserDeleteView(DeleteView):
    model = UserProfile
    template_name = 'admin_panel/user_confirm_delete.html'
    success_url = reverse_lazy('admin_panel:user_list')







# Kategoriyalar uchun view'lar
class CategoryListView(ListView):
    model = Category
    template_name = 'admin_panel/category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(CreateView):
    model = Category
    template_name = 'admin_panel/category_form.html'
    fields = ['name']  # Faqat name maydonini ko'rsatamiz
    success_url = reverse_lazy('admin_panel:category_list')

    def form_valid(self, form):
        # Slugni avtomatik yangilash
        form.instance.slug = slugify(form.instance.name)
        return super().form_valid(form)

class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'admin_panel/category_form.html'
    fields = ['name']  # Faqat name maydonini ko'rsatamiz
    success_url = reverse_lazy('admin_panel:category_list')

    def form_valid(self, form):
        # Slugni avtomatik yangilash
        form.instance.slug = slugify(form.instance.name)
        return super().form_valid(form)

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'admin_panel/category_confirm_delete.html'
    success_url = reverse_lazy('admin_panel:category_list')

# Mahsulotlar uchun view'lar
class ProductListView(ListView):
    model = Product
    template_name = 'admin_panel/product_list.html'
    context_object_name = 'products'

class ProductCreateView(CreateView):
    model = Product
    template_name = 'admin_panel/product_form.html'
    fields = ['category', 'name', 'slug', 'image', 'description', 'price', 'discount', 'rating', 'available']
    success_url = reverse_lazy('admin_panel:product_list')

    def form_valid(self, form):
        # Slugni avtomatik yangilash
        form.instance.slug = slugify(form.instance.name)
        return super().form_valid(form)

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'admin_panel/product_form.html'
    fields = ['category', 'name']  # Faqat name va category ko'rsatiladi
    success_url = reverse_lazy('admin_panel:product_list')

    def form_valid(self, form):
        # Slugni avtomatik yangilash
        form.instance.slug = slugify(form.instance.name)
        return super().form_valid(form)

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'admin_panel/product_confirm_delete.html'
    success_url = reverse_lazy('admin_panel:product_list')
