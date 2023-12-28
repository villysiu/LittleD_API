from django.urls import path 
from . import views 
  
urlpatterns = [ 
    path('categories', views.Categories.as_view()),
]