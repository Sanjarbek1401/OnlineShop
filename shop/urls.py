from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list,
         name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail,
         name='product_detail'),
    path('<int:id>/<slug:slug>/comments/', views.all_comments,name='all_comments'),
 ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
