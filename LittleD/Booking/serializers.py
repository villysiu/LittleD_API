from rest_framework import serializers 
from .models import Reservation
import datetime
import pytz
class ReservationSerializer(serializers.ModelSerializer):


    class Meta:
        model = Reservation
        fields = ['pk','user_id', 'no_of_guests', 'reservation_date', 'reservation_time']
    
    def create(self, validated_data): 

        # Should always return a user since only authenticated user can access ( isAuthenticated)
        user = self.context['request'].user
        print("in create")
        print(validated_data)

        reservation_obj = Reservation.objects.create(user=user, **validated_data)
        reservation_obj.save()
        return reservation_obj
        
    def update(self, instance, validated_data):
        menuitem = instance.menuitem