from django.urls import path 
from . import views 
  
urlpatterns = [ 
    path('categories', views.Categories.as_view()),
    path('categories/<int:pk>', views.SingleCategory.as_view()),

]