from rest_framework import permissions

class MenuItemsPermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated and request.user.groups.filter(name='Manager').exists()
        else:
            return True
    

class MenuItemPermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        
        if request.method in ['DELETE', 'PATCH','PUT']:
            return request.user.is_authenticated and request.user.groups.filter(name='Manager').exists()
        else: # request.method == 'GET':
            return True

class CartItemsPermission(permissions.BasePermission):
    """
        manager can filter the queryset by user_id
        user can see cart with cartitems added by user
        user can add item to cart
    """
    def has_permission(self, request, view):
        user_id = request.query_params.get('user_id')
        if user_id and not request.user.groups.filter(name='Manager').exists():
            return False
        return True


class SingleCartItemPermission(permissions.BasePermission):
    """
        manager can see, update and destroy all cartitem
        user can see, update and destroy cartitem if belonged to user
    """
    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name='Manager').exists() or request.user.id == obj.user.id
    
class OrdersPermission(permissions.BasePermission):     
    '''
        Only manager can filter orders by user_id
    '''
    def has_permission(self, request, view):
        user_id = request.query_params.get('user_id')
        if user_id and not request.user.groups.filter(name='Manager').exists():
            return False
        
        return True
    
class SingleOrderPermission(permissions.BasePermission):
    '''
        manager can see, update and destroy the single order
        user can see the single order if belonged to him
    '''
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='Manager').exists():
            return True
        else:
            return request.method == 'GET' and request.user.id == obj.user.id
            
class SingleOrderItemPermission(permissions.BasePermission):
    '''
        Only manager can see, update and destroy the single order item
    '''
    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name='Manager').exists()
        
            