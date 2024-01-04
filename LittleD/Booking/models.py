from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

from django.utils.translation import gettext_lazy as _
# Create your models here.
class Reservation(models.Model):
    
    def current_dt():
        print("minus 8 hours??")
        print(datetime.datetime.now()-datetime.timedelta(hours=8))
        return datetime.datetime.now()-datetime.timedelta(hours=8)

    def reservation_date_validator(res_date):
        current_dt = datetime.datetime.now()-datetime.timedelta(hours=8)
        if res_date < current_dt.date():
            raise ValidationError(
                "Ensure the value is greater than or equal to {}".format(current_dt.date())
            )

        if res_date > current_dt.date()+datetime.timedelta(days=30):
            raise ValidationError(
                "Ensure the value is smaller than or equal to {}".format(current_dt.date()+datetime.timedelta(days=30))
            )
        
        
    def reservation_time_validator(res_time):
       
        if not (11 <= res_time.hour <= 20):
            raise ValidationError(
                "Ensure the value is between 11:00:00 and 20:00:00"
            )
    

    def next_hour():
        
        next = datetime.datetime.now()-datetime.timedelta(hours=7)
        return '{}:00:00'.format(next.hour)
  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    reservation_date = models.DateField(default = current_dt
                                        # timezone.now
                                        , validators=[reservation_date_validator]
                                        )
    reservation_time = models.TimeField(default = next_hour, validators=[reservation_time_validator])
    no_of_guests = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)], default=1
    )
    
    class Meta:
        unique_together = ('reservation_date', 'reservation_time')
        ordering = ['reservation_date', 'reservation_time']
        

    def __str__(self): 
        return str(self.reservation_date) +" "+str(self.reservation_time)
    