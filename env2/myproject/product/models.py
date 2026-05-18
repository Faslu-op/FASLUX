from django.db import models

# Create your models here.

from django.db import models


class Size(models.Model):
    name = models.CharField(max_length=10)  

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=50) 

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)

    long_description = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    sizes = models.ManyToManyField(Size, blank=True)
    materials = models.ManyToManyField(Material, blank=True)

    def __str__(self):
        return self.name

class New(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name
    

