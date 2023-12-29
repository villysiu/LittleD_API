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
    category = serializers.StringRelatedField()
    class Meta:
        model = MenuItem
        fields = ['pk', 'title',  'year', 'price', 'category', 'varietal','origin', 'point', 'description',
                  'category_id']
    
     # POST
    def create(self, validated_data):
        category = validated_data.pop('Category')
        menuitem_obj = MenuItem.objects.create(category=category, **validated_data)
        return menuitem_obj
    #PATCH/ PUT
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.price = validated_data.get('price', instance.price)
        instance.category = validated_data.get('Category', instance.category)
        instance.featured = validated_data.get('featured', instance.featured)
 
        instance.save()
        return instance
        
        