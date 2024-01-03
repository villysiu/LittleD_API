from django.db import models
from django.contrib.auth.models import User
# from datetime import date
import datetime
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

# Create your models here.
class Reservation(models.Model):

    def reservation_date_validator(res_date):
        if res_date <= datetime.datetime.now().date():
            raise ValidationError(
                "Ensure the value is greater than or equal to {}".format(datetime.datetime.now().date())
            )
        
    def reservation_time_validator(res_time):
        if not (11 <= res_time.hour <= 20):
            raise ValidationError(
                "Ensure the value is between 11:00:00 and 20:00:00"
            )

    def next_hour():
        next = datetime.datetime.now().hour+1
        return '{}:00:00'.format(next)
  
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    
    reservation_date = models.DateField(default = timezone.now, validators=[reservation_date_validator])
    reservation_time = models.TimeField(default = next_hour, validators=[reservation_time_validator])
    no_of_guests = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)], default=1
    )

    # def __str__(self): 
    #     return self.user.username
    