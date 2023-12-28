from django.shortcuts import render
from .models import MenuItem, Category
from .serializers import CategorySerializer, MenuItemSerializer
from rest_framework import generics
# Create your views here.
class Categories(generics.ListCreateAPIView):   
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [CategoriesMenuItemsPermission]

class SingleCategory(generics.RetrieveUpdateDestroyAPIView):   
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [CategoryMenuItemPermission]


class MenuItems(generics.ListCreateAPIView):   
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = MenuItemSerializer
    # permission_classes = [CategoriesMenuItemsPermission]

    # pagination_class = CustomPagination
    ordering_fields=['price', 'point', 'year']
    search_fields = ['title','category__title', 'varietal', 'origin']

    def get_queryset(self):
        queryset = MenuItem.objects.select_related('category').all()
        category_name = self.request.query_params.get('category')
        if category_name:
            queryset = queryset.filter(category__slug=category_name)
        return queryset

    
class SingleMenuItem(generics.RetrieveUpdateDestroyAPIView):   
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    # permission_classes = [CategoryMenuItemPermission]

