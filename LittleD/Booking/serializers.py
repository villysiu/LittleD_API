from rest_framework import serializers 
from .models import Reservation
import datetime

class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ['pk','user_id', 'no_of_guests', 'reservation_date', 'reservation_time']
    
    def create(self, validated_data): 

        # Should always return a user since only authenticated user can access ( isAuthenticated)
        user = self.context['request'].user
        res_dt = datetime.datetime.combine(validated_data['reservation_date'], validated_data['reservation_time'])
        if res_dt < datetime.datetime.now()-datetime.timedelta(hours=8):
            raise serializers.ValidationError(
                "The date and time are not available."
            ) 
        
        reservation_obj = Reservation.objects.create(user=user, **validated_data )
        return reservation_obj
        
    # def update(self, instance, validated_data):
    #     menuitem = instance.menuitem