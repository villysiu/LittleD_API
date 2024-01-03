from django.urls import path
from . import views


urlpatterns = [
    path('', views.Reservations.as_view()),
    path('<int:pk>', views.SingleReservation.as_view()),
]