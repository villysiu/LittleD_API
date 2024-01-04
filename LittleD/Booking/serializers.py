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
        
    def update(self, instance, validated_data):
        # print(validated_data)
        res_date = validated_data.get('reservation_date', instance.reservation_date)
        res_time = validated_data.get('reservation_time', instance.reservation_time)
        
        res_dt = datetime.datetime.combine(res_date, res_time)
        if res_dt < datetime.datetime.now()-datetime.timedelta(hours=8):
            raise serializers.ValidationError(
                "The date and time are not available."
            ) 
        instance.reservation_date = res_date
        instance.reservation_time = res_time
        instance.no_of_guests = validated_data.get('no_of_guests', instance.no_of_guests)
        instance.save()
        return instance