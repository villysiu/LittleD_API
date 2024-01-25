from django.shortcuts import render
from .models import Reservation
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
# from rest_framework.decorators import permission_classes
from .serializers import ReservationSerializer
import datetime
from .permissions import SingleReservationPermission, ReservationPermission
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
            print(upcoming)
            if upcoming == 'true':
                queryset = queryset.filter(reservation_date__gte=datetime.datetime.now()-datetime.timedelta(hours=8))
            else:
                queryset = queryset.filter(reservation_date__lt=datetime.datetime.now()-datetime.timedelta(hours=8))
        return queryset

class SingleReservation(generics.RetrieveUpdateDestroyAPIView):   
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated, SingleReservationPermission]


