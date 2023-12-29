from rest_framework import permissions

class CategoriesMenuItemsPermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        # if request.method == 'GET':
        #     return True
        # elif 
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
           