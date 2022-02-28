from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    image = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, db_constraint=False)

    def __str__(self):
        return self.name