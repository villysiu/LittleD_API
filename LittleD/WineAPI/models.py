from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from django.core.exceptions import ValidationError
class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True)

    # for serializers.StringRelatedField to display string
    def __str__(self)-> str:
        return self.title


class MenuItem(models.Model):
    def year_validator(value):
        if value < 1900 or value > datetime.datetime.now().year:
            raise ValidationError(
                "The year has to be between 1900 and %(value)s", params={"value": datetime.datetime.now().year},
            )
      
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
    origin = models.CharField(max_length=255)
    point = models.PositiveSmallIntegerField(
        blank=True, null=True,
        validators=[MaxValueValidator(100)]
    )
    varietal = models.CharField(max_length=255)
    description = models.TextField()
    year = models.PositiveSmallIntegerField(
        validators=[year_validator], 
    )

    def __str__(self):
        return str(self.year)+ " "+self.title