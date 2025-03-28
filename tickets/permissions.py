from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

User = get_user_model()  

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        
        user  = User.objects.get(id = request.user.id)
        
        if user.role !="super admin":
            raise PermissionDenied(
                {
                    "message":"You must be super admin to perform this operation "
                },

            )
        return True
    
class IsAdmin(permissions.BasePermission):
     def has_permission(self, request, view):
        user = User.objects.get(id = request.user.id)
        if user.role == 'user' : 
            raise PermissionDenied({"message":"You must have admin role to perform this operation"})
        return True