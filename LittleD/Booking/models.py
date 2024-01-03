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
        if res_date < datetime.datetime.now().date():
            raise ValidationError(
                "Ensure the value is greater than or equal to {}".format(datetime.datetime.now().date())
            )

        if res_date > datetime.datetime.now().date()+datetime.timedelta(days=30):
            raise ValidationError(
                "Ensure the value is smaller than or equal to {}".format(datetime.datetime.now().date()+datetime.timedelta(days=30))
            )
        
        
    def reservation_time_validator(res_time):

        if not (11 <= res_time.hour <= 20):
            raise ValidationError(
                "Ensure the value is between 11:00:00 and 20:00:00"
            )
    # def save(self, *args, **kwargs):
    #     self.full_clean()
    #     return super(Reservation, self).save(*args, **kwargs)
    
    # def clean(self):
    #     print("cleannnnnn")
    #     print(self)
    #     print(self.reservation_date)
    #     print(self.reservation_time)
    #     print(datetime.datetime.now())
    #     res = datetime.datetime.combine(self.reservation_date, self.reservation_time)
    #     print(res)
    #     print(res < datetime.datetime.now())
    #     if res < datetime.datetime.now():
    #         error={}
    #         error['sss'] = 'Measurement is outside the run'
    #         raise ValidationError(error['sss'])
    #         # raise ValidationError(
    #         #     "Ensure the date and time are in the future."
    #         # )


    def next_hour():
        next = datetime.datetime.now().hour+1
        return '{}:00:00'.format(next)
  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    reservation_date = models.DateField(default = timezone.now, validators=[reservation_date_validator])
    reservation_time = models.TimeField(default = next_hour, validators=[reservation_time_validator])
    no_of_guests = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)], default=1
    )
    
    # def __str__(self): 
    #     return self.user.username
    