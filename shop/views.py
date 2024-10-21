from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Comment
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from cart.forms import CartAddProductForm
from .forms import CommentModelForm

# Mahsulotlarga like bosish funksiyasi
@login_required
def product_like(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user in product.users_like.all():
        product.users_like.remove(request.user)
        liked = False
    else:
        product.users_like.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'likes_count': product.users_like.count()})

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    # Qidiruv so'rovini olish
    query = request.GET.get('q')
    if query:
        # Qidiruv Product va Category name bo'yicha
        products = products.filter(name__icontains=query) | Product.objects.filter(category__name__icontains=query)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products,
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()

    # Faqat faol izohlarni olish
    active_comments = product.comments.filter(is_active=True).order_by('-created')

    # Umumiy izohlar sonini olish
    total_comments = active_comments.count()

    # Maksimal 3 ta izohni olish
    comments = active_comments[:3]

    new_comment = None

    # Yangi izohni qabul qilish
    if request.method == 'POST':
        comment_form = CommentModelForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.product = product
            new_comment.is_active = True
            new_comment.save()
            # Izoh qo'shilgandan so'ng sahifani qayta yuklash
            return redirect('shop:product_detail', id=product.id, slug=product.slug)
    else:
        comment_form = CommentModelForm()

    return render(request, 'shop/product/detail.html', {
        'product': product,
        'cart_product_form': cart_product_form,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'total_comments': total_comments,
        # Yoqtirish qismi uchun qo'shildi
        'likes_count': product.users_like.count(),
        'is_liked': request.user in product.users_like.all(),
    })

def all_comments(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    comments = Comment.objects.filter(product=product, is_active=True)

    return render(request, 'shop/product/all_comments.html', {
        'product': product,
        'comments': comments
    })
