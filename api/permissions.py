from rest_framework import permissions


class IsStudentType(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.user_type == 'student')
    

class IsEmployerType(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.user_type == 'employer')
    
    