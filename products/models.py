from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField("Назва", max_length=100)
    slug = models.SlugField("URL-мітка", max_length=100, unique=True)

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, 
        related_name='products', 
        on_delete=models.CASCADE, 
        verbose_name="Категорія"
    )
    title = models.CharField("Назва", max_length=255)
    slug = models.SlugField("URL-мітка", max_length=255, unique=True)
    description = models.TextField("Опис", blank=True)
    price = models.DecimalField("Ціна", max_digits=10, decimal_places=2)
    image = models.ImageField("Зображення", upload_to='products/%Y/%m/%d/', blank=True)
    available = models.BooleanField("Доступно", default=True)
    created_at = models.DateTimeField("Дата створення", auto_now_add=True)
    updated_at = models.DateTimeField("Дата оновлення", auto_now=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.slug})


class ViewedProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='views')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Переглянутий товар"
        verbose_name_plural = "Переглянуті товари"
        ordering = ['-viewed_at']
        