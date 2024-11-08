from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# from django.core.exceptions import ValidationError

class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True)
    desc = models.TextField(blank=True, null=True)
    # image_url = models.URLField(max_length=200, blank=True, null=True)
    image_path = models.CharField(max_length=255, blank=True, null=True)
    # for serializers.StringRelatedField to display string
    def __str__(self)-> str:
        return self.title

class Milk(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(
        max_digits=6, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )
    # for serializers.StringRelatedField to display string
    def __str__(self)-> str:
        return self.title

# class Temperature(models.Model):
#     slug = models.SlugField()
#     title = models.CharField(max_length=255, db_index=True)
#     # price = models.DecimalField(
#     #     max_digits=6, decimal_places=2, default=0, validators=[MinValueValidator(0)]
#     # )
#     # for serializers.StringRelatedField to display string
#     def __str__(self)-> str:
#         return self.title
    
class MenuItem(models.Model):      
    TEMP_CHOICES = {
        "N": "Not Changable",
        "H":"Hot",
        "I":"Iced",
    }
    SWEETNESS_CHOICES = {
        "N": "Not Changable",
        "100":"100%",
        "75":"75%",
        "50":"50%",
        "25":"25%",
        "0":"0%"
    }
    
    title = models.CharField(max_length=255, db_index=True)
    image_path = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(
        max_digits=6, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )
    # categories = models.ManyToManyField(Category, through='MenuitemCategory')
    
    description = models.TextField(blank=True, null=True)
    
    inventory = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(1000)], default=0
    )
    milk = models.ForeignKey(Milk, on_delete=models.PROTECT, null=True, blank=True)
    temperature = models.CharField(max_length=1, choices=TEMP_CHOICES, default="I")
    sweetness = models.CharField(max_length=3, choices=SWEETNESS_CHOICES, default="100")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
    # temperature = models.ForeignKey(Temperature, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.title

# class MenuitemCategory(models.Model):
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)

#     class Meta: 
#         unique_together = ('category', 'menuitem')
#     def __str__(self):
#         return "{}_{}".format(self.menuitem.__str__(), self.category.__str__())
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE, db_index=True)
    quantity = models.PositiveSmallIntegerField(default=0)
    milk = models.ForeignKey(Milk, on_delete=models.PROTECT, null=True, blank=True)
    temperature = models.CharField(max_length=1, default='I')
    sweetness = models.CharField(max_length=3, default='100')
    
    class Meta: 
        unique_together = ('menuitem', 'milk', 'user','temperature', 'sweetness')

    
class Order(models.Model):
    STATUS_CHOICES = {
        "R":"Received",
        "P":"Processing",
        "S": "Served"
    }
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    order_status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="R")
    
    # total = models.DecimalField(decimal_places=2, max_digits=5, default=0, editable=False)
    date = models.DateField(db_index=True, null=True, blank=True)
    tip = models.DecimalField(decimal_places=2, max_digits=5, default=0)
 
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='orderitems', on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    # unit_price = models.DecimalField(decimal_places=2, max_digits=5, default=0, editable=False)
    # line_total = models.DecimalField(decimal_places=2, max_digits=5, default=0, editable=False)
    milk = models.ForeignKey(Milk, on_delete=models.PROTECT, null=True, blank=True)
    temperature = models.CharField(max_length=1, default='I')
    sweetness = models.CharField(max_length=3, default='100')
    class Meta:
        unique_together = ('order', 'menuitem', 'milk', 'temperature', 'sweetness')

