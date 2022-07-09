from django.db import models
from app_base.models import Product
from django.contrib.auth import get_user_model
User = get_user_model()


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    publish_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.phone


class ProductCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True)
