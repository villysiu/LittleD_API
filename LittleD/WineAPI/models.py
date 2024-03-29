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
    price = models.DecimalField(
        max_digits=6, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
    origin = models.CharField(max_length=255, blank=True, null=True)
    point = models.PositiveSmallIntegerField(
        blank=True, null=True, validators=[MaxValueValidator(100)]
    )
    varietal = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    year = models.PositiveSmallIntegerField(
        validators=[year_validator], 
    )
    inventory = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(1000)], default=0
    )

    def __str__(self):
        return str(self.year)+ " "+self.title
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE, db_index=True)
    quantity = models.PositiveSmallIntegerField(default=0)
   

    
class Order(models.Model):
    STATUS_CHOICES = {
        "R":"Received",
        "P":"Processing",
        "S": "Shipped"
    }
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    order_status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="R")
    
    total = models.DecimalField(decimal_places=2, max_digits=5, default=0, editable=False)
    # date = models.DateTiField(db_index=True, null=True, blank=True)
    date = models.DateField(db_index=True, null=True, blank=True)
 
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='orderitems', on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    unit_price = models.DecimalField(decimal_places=2, max_digits=5, default=0, editable=False)
    line_total = models.DecimalField(decimal_places=2, max_digits=5, default=0, editable=False)
  
    class Meta:
        unique_together = ('order', 'menuitem')

