import pytz
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from shop.models import Category, Product,UserProfile
from django import forms
from django.urls import reverse_lazy
from django.utils.text import slugify
from orders.models import Order, OrderItem
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from openpyxl import Workbook


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('admin_panel:dashboard')  # admin_panel uchun yo'naltirish
    else:
        form = AuthenticationForm()
    return render(request, 'admin_panel/login.html', {'form': form})


@login_required()
def dashboard(request):
    # Foydalanuvchi `staff` ekanligini tekshirish
    if not request.user.is_staff:
        return redirect('login')  # Agar `staff` bo'lmasa, login sahifasiga yo'naltiriladi
    return render(request, 'admin_panel/dashboard.html')  # Admin panel dashboard sahifasi

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
    fields = ['category', 'name', 'slug', 'image', 'description', 'price', 'discount', 'rating', 'available']
    success_url = reverse_lazy('admin_panel:product_list')

    def form_valid(self, form):
        # Slugni avtomatik yangilash
        form.instance.slug = slugify(form.instance.name)
        return super().form_valid(form)

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'admin_panel/product_confirm_delete.html'
    success_url = reverse_lazy('admin_panel:product_list')




# Orderlarni ro'yxatini ko'rish va statuslarni yangilash
class OrderListView(ListView):
    model = Order
    template_name = 'admin_panel/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')  # GET parametrini oling

        if status:
            queryset = queryset.filter(status=status)  # Status bo'yicha filtrlash

        return queryset

class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'admin_panel/order_form.html'
    fields = ['status']
    success_url = reverse_lazy('admin_panel:order_list')

class OrderDetailView(DetailView):
    model = Order
    template_name = 'admin_panel/order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = OrderItem.objects.filter(order=self.object)
        return context

def export_orders_to_xlsx(request):
    # Excel faylini yaratish
    wb = Workbook()
    ws = wb.active
    ws.title = "Buyurtmalar"

    # Sarlavhalar qo'shish
    headers = [
        "ID", "Ism", "Familiya", "Email", "Manzil", "Shahar", "Status", "Yaratilgan Vaqti"
    ]
    ws.append(headers)

    # Status filtri olish
    status = request.GET.get('status', '')
    if status:
        orders = Order.objects.filter(status=status)
    else:
        orders = Order.objects.all()

    # O'zbekiston vaqt zonasi
    uz_tz = pytz.timezone('Asia/Tashkent')

    for order in orders:
        # O'zbekiston vaqtiga o'tkazish
        created_uz = order.created.astimezone(uz_tz)  # UTC dan O'zbekistonga o'tkazish

        ws.append([
            order.id,
            order.first_name,
            order.last_name,
            order.email,
            order.address,
            order.city,
            order.get_status_display(),
            created_uz.strftime('%Y-%m-%d %H:%M:%S'),  # O'zbekiston vaqtini formatlash
        ])

    # Response tayyorlash
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="buyurtmalar.xlsx"'
    wb.save(response)

    return response
