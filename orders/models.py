from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    first_name = models.CharField("Ім'я", max_length=50)
    last_name = models.CharField("Прізвище", max_length=50)
    address = models.CharField("Адреса доставки", max_length=250)
    phone = models.CharField("Номер телефону", max_length=20)
    
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"

    def __str__(self):
        return f"Замовлення #{self.id} від {self.user.username}"
