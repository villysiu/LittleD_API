from rest_framework import serializers 
from .models import Category, MenuItem, Cart, OrderItem, Order, Milk, MenuitemCategory
from datetime import date
from django.db.models import Sum, ExpressionWrapper,F, DecimalField
from decimal import *
from django.db import IntegrityError

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['pk','title', 'slug']

class MilkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milk
        fields = "__all__"


class MenuItemSerializer(serializers.ModelSerializer):
    
    milk_pk = serializers.PrimaryKeyRelatedField(
        source='Milk',
        queryset=Milk.objects.all(), 
        write_only=True,
    )
    temperature = serializers.CharField()
    sweetness = serializers.CharField()
    # temperature = serializers.CharField(source='get_temperature_display')
    # order_status = serializers.CharField(source='get_order_status_display', read_only=True)
    class Meta:
        model = MenuItem
        fields = ['pk', 'title', 'price', 'description',
                  'inventory', 'milk_id', 'milk_pk', 'temperature', 'sweetness']
    
   
    # POST
    def create(self, validated_data):
        print("in serializer")
        print(validated_data)
        milk_obj = validated_data.pop('Milk')
        menuitem_obj = MenuItem.objects.create( milk=milk_obj, **validated_data)
        return menuitem_obj
    
    # #PATCH/ PUT
    def update(self, instance, validated_data):
        print(validated_data)
        instance.title = validated_data.get('title', instance.title)
        instance.price = validated_data.get('price', instance.price)
        instance.description = validated_data.get('description', instance.description)
        instance.inventory = validated_data.get('inventory', instance.inventory)
        instance.milk = validated_data.get('Milk', instance.milk)
        instance.temperature = validated_data.get('temperature', instance.temperature)
        instance.sweetness = validated_data.get('sweetness', instance.sweetness)
        instance.save()
        return instance

class MenuitemCategorySerializer(serializers.ModelSerializer):
    menuitem_pk = serializers.PrimaryKeyRelatedField(
        source='MenuItem',
        queryset=MenuItem.objects.all(), 
        write_only=True,
    )
    category_pk = serializers.PrimaryKeyRelatedField(
        source='Category',
        queryset=Category.objects.all(), 
        write_only=True,
    )
    menuitem = MenuItemSerializer(read_only=True)
    class Meta:
        model = MenuitemCategory
        fields = [ "pk","menuitem_pk", "category_pk", 'category_id', 'menuitem_id', 'menuitem']

    def create(self, validated_data): 
        print(validated_data)
        menuitem = validated_data.pop('MenuItem')
        category = validated_data.pop('Category')
        menuitem_category_obj = MenuitemCategory.objects.create(menuitem=menuitem, category=category)
        
        menuitem_category_obj.save()
        return menuitem_category_obj

    def update(self, instance, validated_data):
        instance.menuitem = validated_data.get('MenuItem', instance.menuitem)
        instance.category = validated_data.get('Category', instance.category)
        instance.save()
        return instance

    
class CartSerializer(serializers.ModelSerializer):

    menuitem_pk = serializers.PrimaryKeyRelatedField(
        source='MenuItem',
        queryset=MenuItem.objects.all(), 
        write_only=True,
    )
    milk_pk = serializers.PrimaryKeyRelatedField(
        source='Milk',
        queryset=Milk.objects.all(), 
        write_only=True,
    )
    temperature = serializers.CharField()
    sweetness = serializers.CharField()
    unit_price = serializers.SerializerMethodField()
    linetotal = serializers.SerializerMethodField()
    tax = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['pk','user_id', 
                  'menuitem_pk', 'menuitem_id', 
                  'quantity','linetotal', 'unit_price','tax',
                  'milk_id', 'milk_pk', 'temperature', 'sweetness']

    def get_unit_price(self, obj):
        return obj.menuitem.price + obj.milk.price
    
    def get_linetotal(self, obj):
        print('in linetotal')
       
        return obj.quantity * self.get_unit_price(obj)
        
    def get_tax(self, obj):
        return self.get_linetotal(obj) * Decimal('0.1')

    def create(self, validated_data): 
        # Should always return a user since only authenticated user can access ( isAuthenticated)
        print(validated_data)
        user = self.context['request'].user
        menuitem = validated_data.pop('MenuItem')
        milk = validated_data.pop('Milk')
        temperature = validated_data.pop('temperature')
        sweetness = validated_data.pop('sweetness')
        cartitem_obj, created =Cart.objects.get_or_create(menuitem=menuitem, user=user, milk=milk, temperature=temperature, sweetness=sweetness)
        if menuitem.inventory <= cartitem_obj.quantity:
            cartitem_obj.delete()
            raise serializers.ValidationError("Out of stock".format(menuitem.inventory))
        
        cartitem_obj.quantity += validated_data.get('quantity', 1)
        
        cartitem_obj.save()
        return cartitem_obj
        
    def update(self, instance, validated_data):
        print(validated_data)
        user = self.context['request'].user
        menuitem = instance.menuitem
        
        if 'quantity' in validated_data and menuitem.inventory  < validated_data['quantity']:
            raise serializers.ValidationError("There is only {} in stock".format(menuitem.inventory))

        try:
            instance.quantity = validated_data.get('quantity', instance.quantity)  
            instance.milk = validated_data.get('Milk', instance.milk)
            instance.temperature = validated_data.get('temperature', instance.temperature)
            instance.sweetness = validated_data.get('sweetness', instance.sweetness)
            instance.save()
            return instance

        except IntegrityError as e:
            print("Item with same spec existed")
            milk = validated_data.get('Milk', instance.milk)
            temperature = validated_data.get('temperature', instance.temperature)
            sweetness = validated_data.get('sweetness', instance.sweetness)
            dup_cartitem =Cart.objects.get(menuitem=menuitem, user=user, milk=milk, temperature=temperature, sweetness=sweetness)
            
            dup_cartitem.quantity += instance.quantity
            dup_cartitem.save()
            instance.delete()
            
            return dup_cartitem
       
    
class OrderItemSerializer(serializers.ModelSerializer):   
   
    # menuitem = serializers.PrimaryKeyRelatedField(read_only=True)
    menuitem_pk = serializers.PrimaryKeyRelatedField(
        source='MenuItem',
        queryset=MenuItem.objects.all(), 
        write_only=True,
    )
    # milk = serializers.StringRelatedField(read_only=True)
    milk_pk = serializers.PrimaryKeyRelatedField(
        source='Milk',
        queryset=Milk.objects.all(), 
        write_only=True,
    )
    temperature = serializers.CharField()
    sweetness = serializers.CharField()
    unit_price = serializers.SerializerMethodField(read_only=True)
    line_total = serializers.SerializerMethodField(read_only=True)
    # title = serializers.SerializerMethodField(read_only=True)
    # unit_price = serializers.FloatField()
    # line_total = serializers.FloatField()

    class Meta:
        model = OrderItem
        fields = [ 
            'pk', 'menuitem_id', 'menuitem_pk',
            'quantity', 'unit_price', 'line_total',
            'milk_id', 'milk_pk', 'temperature', 'sweetness'
            ]
        
    def get_unit_price(self, obj):
        return obj.menuitem.price + obj.milk.price
    
    def get_line_total(self, obj):
        return obj.quantity * self.get_unit_price(obj)

    # def get_title(self, obj):
    #     return obj.menuitem.title

    
    def update(self, instance, validated_data):
        menuitem = instance.menuitem
        if menuitem.inventory + instance.quantity < validated_data['quantity']:
            raise serializers.ValidationError("oh no There is {} in stock".format(menuitem.inventory))
        
        menuitem.inventory = menuitem.inventory+instance.quantity-validated_data['quantity']
        menuitem.save()

        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
       
        return instance

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    orderitems = OrderItemSerializer(many=True)
    order_status = serializers.CharField(source='get_order_status_display', read_only=True)
    subtotal = serializers.SerializerMethodField(read_only=True)
    tax = serializers.SerializerMethodField(read_only=True)
    total = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Order
        fields = ['pk', 'user', 'date', 'order_status', 'subtotal',
                  'tax', 'tip', 'total', 'orderitems']

    def get_subtotal(self, obj):
    
        value = obj.orderitems.aggregate(total=Sum(
            ExpressionWrapper(
                F('quantity') * (F('menuitem__price') + F('milk__price')), 

                output_field=DecimalField()
        )))['total']
    
        return value
    
    def get_tax(self, obj):
        return self.get_subtotal(obj) * Decimal('0.1')

    def get_total(self, obj):
        return self.get_subtotal(obj) * Decimal('1.1') + obj.tip
   

    def create(self, validated_data):
        print('in order serualizer')
    
        print(validated_data)
    #    {'tip': Decimal('0.75'), 'orderitems': [OrderedDict([('MenuItem', <MenuItem: Jasmine Milk Tea>), ('quantity', 1), ('Milk', <Milk: Whole Milk>)])]}
        orderitems = validated_data.pop('orderitems')
        # print(orderitems)
        # [OrderedDict([('MenuItem', <MenuItem: Boba Black Milk Tea>), ('quantity', 3), ('Milk', <Milk: Soy Milk>)])]
        user = self.context['request'].user

        order_obj = Order.objects.create(user=user, date=date.today(), tip=validated_data['tip'])
    
    
        for orderitem in orderitems:
            menuitem = orderitem.pop('MenuItem')
            milk = orderitem.pop('Milk')

            if orderitem['quantity'] > menuitem.inventory:
                raise serializers.ValidationError("There is only {} of {} in stock.".format(menuitem.name, menuitem.inventory))
            # update inventory 
            menuitem.inventory -= orderitem['quantity']
            menuitem.save()
            OrderItem.objects.create(order=order_obj, menuitem=menuitem, milk=milk, **orderitem )
            
        order_obj.save()
        return order_obj



    def update(self, instance, validated_data):
        print(validated_data)
        instance.order_status = validated_data.get('order_status', instance.order_status)
        instance.save()
        return instance

    