from rest_framework import permissions

class ReservationPermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated
        else:
            return True
    
