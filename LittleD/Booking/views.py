from django.shortcuts import render
from .models import Reservation
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
# from rest_framework.decorators import permission_classes
from .serializers import ReservationSerializer
from datetime import datetime
# Create your views here.
class Reservations(generics.ListCreateAPIView):   
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    # queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    ordering_fields=['reservation_date']
    def get_queryset(self):
        queryset = Reservation.objects.all()
        current_user = self.request.user
        upcoming = self.request.query_params.get('upcoming')
        user_id = self.request.query_params.get('user_id')
        if current_user.groups.filter(name='Manager').exists():
            if user_id:
                queryset = queryset.filter(user__pk=user_id)
  
        else:
            queryset = queryset.filter(user__pk=current_user.id)

        if upcoming:
            queryset = queryset.filter(reservation_date__gte=datetime.today())
        return queryset

class SingleReservation(generics.RetrieveUpdateDestroyAPIView):   
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

