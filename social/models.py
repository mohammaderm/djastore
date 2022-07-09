from django.db import models
from app_base.models import Product
from django.contrib.auth import get_user_model
User = get_user_model()


class Cumment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, null=True)
    value = models.CharField(max_length=400, null=True)
    validation = models.BooleanField(default=False)
    publish_date = models.DateTimeField(auto_now_add=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
