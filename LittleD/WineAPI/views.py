from django.shortcuts import render
from rest_framework.response import Response
from .models import MenuItem, Category, Cart, Order, OrderItem
from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer, OrderItemSerializer
from .permissions import CategoriesMenuItemsPermission, CategoryMenuItemPermission, CartItemPermission, OrderPermission, OrderItemPermission
# , OrdersPermission
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
# Create your views here.
class Categories(generics.ListCreateAPIView):   
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CategoriesMenuItemsPermission]

class SingleCategory(generics.RetrieveUpdateDestroyAPIView):   
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CategoryMenuItemPermission]


class MenuItems(generics.ListCreateAPIView):   
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = MenuItemSerializer
    permission_classes = [CategoriesMenuItemsPermission]

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
    permission_classes = [CategoryMenuItemPermission]

class CartItmes(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        current_user = self.request.user
        queryset = Cart.objects.filter(user=current_user)
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        print("delete cart")
        queryset = self.get_queryset()

        for item in queryset:
            item.delete()
        return Response({'message': 'User Cart is Empty.'}, 204)

class SingleCartItem(generics.RetrieveUpdateDestroyAPIView):   
    serializer_class = CartSerializer
    permission_classes = [CartItemPermission]
    queryset = Cart.objects.all()

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def orders(request):
    if request.method == 'GET':
        queryset = Order.objects.all()
        if request.user.groups.filter(name='Manager').exists():
            status = request.query_params.get('status')
            
            user_id = request.query_params.get('user_id')
            print(user_id)
            if status:
                queryset = queryset.filter(status__slug=status)
            if user_id:
                queryset = queryset.filter(user__pk=user_id)
        
        else:
            queryset = queryset.filter(user=request.user)
        # print(orders)
        # # <QuerySet [<Order: Order object (1)>, <Order: Order object (11)>, <Order: Order object (12)>]>
        
        serialized_orders = OrderSerializer(queryset, many=True)
        return Response(serialized_orders.data, 200)
    
    if request.method == 'POST':
        user_cart_items = Cart.objects.filter(user=request.user)
        #<QuerySet [<Cart: Cart object (14)>, <Cart: Cart object (15)>]>
        if len(user_cart_items) == 0:
            return Response({'message': 'Cart is empty.'}, 200)

        
        orderitems=[]
        for item in list(user_cart_items.values()):
            orderitems.append(item)
        print(orderitems)
        # print(type(orderitems))
        serialized_order = OrderSerializer(
            data = {'orderitems': orderitems}, 
            context = {'request': request}
        )
        
        if serialized_order.is_valid(raise_exception=True):
            serialized_order.save()
            # for user_cart_item in user_cart_items:
            #     user_cart_item.delete()
            return Response(serialized_order.data, 200)
        

class SingleOrder(generics.RetrieveUpdateDestroyAPIView):   
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [OrderPermission]

class SingleOrderItem(generics.RetrieveUpdateDestroyAPIView):   
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [OrderItemPermission]

    

    
    
    