from rest_framework import permissions

class CategoriesMenuItemsPermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated and request.user.groups.filter(name='Manager').exists()
        else:
            return True
    

class CategoryMenuItemPermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        
        if request.method in ['DELETE', 'PATCH','PUT']:
            return request.user.is_authenticated and request.user.groups.filter(name='Manager').exists()
        else: # request.method == 'GET':
            return True
           
class CartItemPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.user.id
    
            
class OrderPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.groups.filter(name='Manager').exists():
            return True
        else:
            return request.method == 'GET' and request.user.is_authenticated and request.user.id == obj.user.id
            
class OrderItemPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.groups.filter(name='Manager').exists()
        
            