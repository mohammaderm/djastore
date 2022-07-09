from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


def image_path(instance, filename):
    return "%s/%s" % (instance.product.name, filename)


def primary_image_path(instance, filename):
    return "%s/%s" % (instance.name, filename)


class Productdiscount(models.Model):
    discount_percent = models.PositiveSmallIntegerField(null=True, default=0,
                                                        validators=[MaxValueValidator(100),
                                                                    MinValueValidator(1)])
    data_status = models.DateTimeField(auto_now_add=False, blank=True, null=True)

    def __str__(self):
        return str(self.discount_percent)


class Category(models.Model):
    name = models.CharField(max_length=100, null=True)
    icon = models.CharField(max_length=100, null=True, blank=True)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'parent',)
        verbose_name_plural = "categories"

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])


class Seller(models.Model):
    name = models.CharField(max_length=100, null=True)
    category = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, null=True)
    category = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.name


class GeneralSpecifications(models.Model):
    name = models.CharField(max_length=100, null=True)
    category = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.name


class SpecificationsValue(models.Model):
    name = models.CharField(max_length=100, null=True)
    generalspecifications = models.ForeignKey(GeneralSpecifications, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return '%s --> %s' % (self.generalspecifications.name, ''.join(self.name))


class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    eng_name = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    publish_date = models.DateTimeField(auto_now_add=True, null=True)
    primary_price = models.PositiveIntegerField(null=True)
    primary_image = models.ImageField(upload_to=primary_image_path, null=True)
    discount_status = models.BooleanField(default=False)
    suggest = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    seller = models.ManyToManyField(Seller)
    specificationsvalue = models.ManyToManyField(SpecificationsValue)
    productdiscount = models.ForeignKey(Productdiscount, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class AttrarName(models.Model):
    name = models.CharField(max_length=100, null=True)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Attrar(models.Model):
    attrarname = models.ForeignKey(AttrarName, null=True, on_delete=models.CASCADE)
    key = models.CharField(max_length=100, null=True)
    value = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.key


class productImage(models.Model):
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_path, null=True)

    def __str__(self):
        return self.product.name
