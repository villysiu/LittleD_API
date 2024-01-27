from django.shortcuts import render
from .models import Reservation
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
# from rest_framework.decorators import permission_classes
from .serializers import ReservationSerializer
import datetime
from .permissions import SingleReservationPermission, ReservationPermission
from django.db.models import DateTimeField, ExpressionWrapper, F
from django.db import models
# Create your views here.
    
class Reservations(generics.ListCreateAPIView):   
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]

    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated, ReservationPermission]
    ordering_fields=['reservation_date']
    filterset_fields = ['reservation_date', 'user_id']
    def get_queryset(self):
        queryset = Reservation.objects.all()
        current_user = self.request.user
        upcoming = self.request.query_params.get('upcoming')
       
        if not current_user.groups.filter(name='Manager').exists():
            queryset = queryset.filter(user__pk=current_user.id)

        if upcoming:
            
            # https://docs.djangoproject.com/en/5.0/topics/db/aggregation/
            current_dt = datetime.datetime.now()-datetime.timedelta(hours=8)
            today = current_dt.date()
            now = current_dt.time()
            print(current_dt)
            print(today)
            print(now)
            current = queryset.filter(
                models.Q(reservation_date__gt=today) | models.Q(
                    reservation_date=today,
                    reservation_time__gt=now
                )
            )
            if upcoming == 'true':
                return current
            else:
                return queryset.exclude(id__in=current)
        return queryset

class SingleReservation(generics.RetrieveUpdateDestroyAPIView):   
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated, SingleReservationPermission]


