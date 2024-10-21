# from tkinter.font import names
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import (
    CategoryListView,
    ProductListView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    UserListView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
    OrderListView,
    OrderUpdateView,
    user_login,
    dashboard,
    OrderDetailView,
    export_orders_to_xlsx

)

app_name = 'admin_panel'

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),

    #For users
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/edit/', UserUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),

    #For orders
    path('orders/',OrderListView.as_view(),name='order_list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('orders/edit/<int:pk>/', OrderUpdateView.as_view(), name='order_edit'),
    path('orders/export/', export_orders_to_xlsx, name='export_orders'),

    # For login
    path('login/',user_login,name='user_login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard, name='dashboard')

]
