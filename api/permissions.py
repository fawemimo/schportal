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
            print(e)


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
            print(e)
