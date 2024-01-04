from rest_framework import permissions
import datetime
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
        # user can see all his reservatopn
        # user can only update or destroy future reservations
        # manager can see reservations of all user 
        # manager can update and destroy past and upcoming reservations
        print("in single res permission")
        if request.user.groups.filter(name='Manager').exists():
            return True
        else:
            if request.method in ['PATCH', 'DESTROY']:
                
                res_dt = datetime.datetime.combine(obj.reservation_date, obj.reservation_time)
                if res_dt < datetime.datetime.now()-datetime.timedelta(hours=8):
                    return False
                
            return request.user.id == obj.user.id
                
        
            
    
