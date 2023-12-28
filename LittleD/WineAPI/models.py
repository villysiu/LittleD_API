from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True)

    # for serializers.StringRelatedField to display string
    def __str__(self)-> str:
        return self.title

    
class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
    origin = models.CharField(max_length=255)
    point = models.IntegerField()
    varietal = models.CharField(max_length=255)
    description = models.TextField()
    year = models.SmallIntegerField()
    def __str__(self):
        return self.title