from rest_framework import serializers 
from .models import Category, MenuItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['pk','title', 'slug']

class MenuItemSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        source='Category',
        queryset=Category.objects.all(), 
        write_only=True,
    )
    # category = serializers.StringRelatedField()
    class Meta:
        model = MenuItem
        fields = ['pk', 'title', 'price', 'category','category_id', 'featured']
       