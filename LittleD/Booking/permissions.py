from rest_framework import permissions

class ReservationPermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        user_id = request.query_params.get('user_id')
        if user_id and not request.user.groups.filter(name='Manager').exists():
            return False
        
        
        return True
        
        
class SingleReservationPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # user can see his own reservatopn and edit
        #  manager can see all res and edit
        if request.user.is_authenticated:
            if request.user.groups.filter(name='Manager').exists():
                return True
            else:
                return request.user.id == obj.user.id
        else:
            return False

        
            
    
