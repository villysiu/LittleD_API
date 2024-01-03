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

        res_date = validated_data['reservation_date']
        res_time = validated_data['reservation_time']
        existed = Reservation.objects.filter(reservation_date=res_date, reservation_time=res_time).exists()

        if existed:
            raise serializers.ValidationError(
                "The day and time slot is not available."
            )
        reservation_obj = Reservation.objects.create(user=user, **validated_data )
        return reservation_obj
        
    def update(self, instance, validated_data):
        menuitem = instance.menuitem