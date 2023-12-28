from django.urls import path 
from . import views 
  
urlpatterns = [ 
    path('categories', views.Categories.as_view()),
    path('categories/<int:pk>', views.SingleCategory.as_view()),

    path('menuitems', views.MenuItems.as_view()),
    path('menuitems/<int:pk>', views.SingleMenuItem.as_view()),

]