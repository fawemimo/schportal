from rest_framework import permissions, status
from rest_framework.response import Response


class IsStudentType(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            if request.user.user_type == "student":
                return bool(request.user and request.user.user_type == "student")
            else:
                return Response(
                    {"error": "Unauthorized user"}, status=status.HTTP_401_UNAUTHORIZED
                )
        except Exception as e:
            pass    

    def has_object_permission(self, request, view, obj):
        try:
            if request.user.user_type == "student":
                return bool(request.user and request.user.user_type == "student")
            else:
                return Response(
                    {"error": "Unauthorized user"}, status=status.HTTP_401_UNAUTHORIZED
                )
        except Exception as e:
            pass 

    def has_permission_denied(self, request, message='Only Student type can access the resources'):
        response_data = {'message': message}
        return Response(response_data, status=status.HTTP_403_FORBIDDEN)       
      

class IsEmployerType(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            if request.user.user_type == "employer":
                return bool(request.user and request.user.user_type == "employer")
            else:
                return Response(
                    {"error": "Unauthorized user"}, status=status.HTTP_401_UNAUTHORIZED
                )
        except Exception as e:
            pass
    
    def has_object_permission(self, request, view, obj):
        try:
            if request.user.user_type == "employer":
                return bool(request.user and request.user.user_type == "employer")
            else:
                return Response(
                    {"error": "Unauthorized user"}, status=status.HTTP_401_UNAUTHORIZED
                )
        except Exception as e:
            pass 

    def has_permission_denied(self, request, message='Only employer type can access the resources'):
        response_data = {'message': message}
        return Response(response_data, status=status.HTTP_403_FORBIDDEN) 