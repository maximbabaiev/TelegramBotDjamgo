from django.db import models


# Create your models here.


class Categorie(models.Model):
    name_categories = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name_categories}"


class ProductModel(models.Model):
    nameProd = models.CharField(max_length=100, unique=True)
    nameCategories = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True)
    value = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"{self.nameProd}"


class Order(models.Model):
    nameProd = models.ForeignKey(ProductModel, on_delete=models.SET_NULL, null=True)
    idUser = models.IntegerField()
    datetime = models.DateTimeField()
    value = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f"{self.nameProd}"
