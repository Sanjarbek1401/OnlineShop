from django.urls import reverse
from django.db import models
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12, unique=True)
    address = models.CharField(max_length=120)

    def __str__(self):
        return self.user.username



class Category(models.Model):
    name = models.CharField(max_length=550)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])




class Product(models.Model):
    class RatingChoices(models.IntegerChoices):
        zero = 0
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5

    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=550)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.IntegerField(default=0)
    rating = models.PositiveIntegerField(choices=RatingChoices.choices, default=RatingChoices.zero)
    users_like = models.ManyToManyField(User, related_name='users_like',null=True, blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.name

    @property
    def discount_priced(self):
        if self.discount > 0:
            return self.price * (Decimal(1) - Decimal(self.discount) / Decimal(100))
        return self.price


    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

    def clean(self):
        if self.discount < 0 or self.discount > 100:
            raise ValidationError('Discount must be between 0 and 100.')



class Comment(models.Model):
    full_name = models.CharField(max_length=550,null=True,blank=True)
    email = models.EmailField()
    message = models.TextField()
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.full_name} ==> by comment'

    class Meta:
        verbose_name_plural = 'Comments'
