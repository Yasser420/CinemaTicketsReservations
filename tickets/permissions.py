from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

User = get_user_model()  # Gets your custom User model

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated: 
            raise PermissionDenied(
                {
                    "status": "error",
                    "code": "not_authenticated",
                    "message": "Authentication credentials were not provided."
                },
                code=401
            )
        
        user  = User.objects.get(id = request.user.id)
        
        if user.role !="super admin":
            raise PermissionDenied(
                {
                    "status": "error",
                    "code": "permission_denied",
                    "message":"You must be super admin to perform this operation "
                },
                code=403
            )
        return True