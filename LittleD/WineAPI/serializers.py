from rest_framework import serializers 
from .models import Category, MenuItem, Cart, OrderItem, Order, OrderStatus
from datetime import datetime
from django.db.models import Sum, ExpressionWrapper,F, DecimalField
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
                  'category_id', 'inventory']
    
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
        instance.year = validated_data.get('year', instance.year)
        instance.varietal = validated_data.get('varietal', instance.varietal)
        instance.origin = validated_data.get('origin', instance.origin)
        instance.point = validated_data.get('point', instance.point)
        instance.description = validated_data.get('description', instance.description)
        instance.inventory = validated_data.get('inventory', instance.inventory)
        instance.save()
        return instance
        
class CartSerializer(serializers.ModelSerializer):
    
    menuitem = serializers.StringRelatedField(read_only=True)
    menuitem_id = serializers.PrimaryKeyRelatedField(
        source='MenuItem',
        queryset=MenuItem.objects.all(), 
        write_only=True,
    )
   
    unit_price = serializers.DecimalField(max_digits=5, decimal_places=2, source='menuitem.price', read_only=True)

    linetotal = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['pk','user_id', 
                  'menuitem', 
                  'quantity', 'menuitem_id', 'linetotal', 'unit_price']

    def get_linetotal(self, obj):
        return '{}'.format(obj.quantity * obj.menuitem.price)
        
    
    def create(self, validated_data): 
        # Should always return a user since only authenticated user can access ( isAuthenticated)
        user = self.context['request'].user
        menuitem = validated_data.pop('MenuItem')

        cartitem_obj, created =Cart.objects.get_or_create(menuitem=menuitem, user=user)
        if menuitem.inventory <= cartitem_obj.quantity:
            raise serializers.ValidationError("There is not enough in stock".format(menuitem.inventory))
        cartitem_obj.quantity += 1
        cartitem_obj.save()
        return cartitem_obj
        
    def update(self, instance, validated_data):
        menuitem = instance.menuitem

        if menuitem.inventory  < validated_data['quantity']:
            raise serializers.ValidationError("There is {} in stock".format(menuitem.inventory))
        
        instance.quantity = validated_data.get('quantity', instance.quantity)  
        instance.save()
        
        
        return instance
    
class OrderItemSerializer(serializers.ModelSerializer):   
    menuitem = serializers.StringRelatedField(read_only=True)
    menuitem_id = serializers.PrimaryKeyRelatedField(
        source='MenuItem',
        queryset=MenuItem.objects.all(), 
        write_only=True,
    )
    line_total = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItem
        fields = [ 
            'pk', 'menuitem_id', 'menuitem', 
            'quantity', 'unit_price', 'line_total' ]
        
    
    def get_line_total(self, obj):
        return obj.quantity * obj.unit_price

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
   
    status = serializers.StringRelatedField(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(
        source='OrderStatus',
        queryset=OrderStatus.objects.all(), 
        write_only=True,
        required=False,
        
    )
    total = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Order
        fields = ['pk', 'user', 'orderitems', 'status', 'total','status_id']

    def get_total(self, obj):
        value = obj.orderitems.aggregate(total=Sum(
            ExpressionWrapper(
                F('quantity') * F('unit_price'),
                output_field=DecimalField()
        )))['total']
    
        return value
    
    def create(self, validated_data):
        print(validated_data)
        # {'orderitems': [OrderedDict([('MenuItem', <MenuItem: 2019 Chester-Kidder>), ('quantity', 2)]), 
        #                 OrderedDict([('MenuItem', <MenuItem: 2020 ACS>), ('quantity', 1)])]}
        orderitems = validated_data.pop('orderitems')
        user = self.context['request'].user
        order_obj = Order.objects.create(user=user, date=datetime.today())
        
        for orderitem in orderitems:
            menuitem = orderitem.pop('MenuItem')

            if orderitem['quantity'] > menuitem.inventory:
                raise serializers.ValidationError("oh no There is {} in stock".format(menuitem.inventory))
            # update inventory 
            menuitem.inventory -= orderitem['quantity']
            menuitem.save()
            OrderItem.objects.create(order = order_obj, menuitem=menuitem, unit_price=menuitem.price, **orderitem )
            
        order_obj.save()
        return order_obj


    def update(self, instance, validated_data):
        instance.status = validated_data.get('OrderStatus', instance.status)
        instance.save()
        return instance

    