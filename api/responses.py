from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
# from djoser.serializers import exceptions as djoser_exceptions


# For serializers
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ValidationError):
        response.data = {
            'message': 'Validation failed',
            'errors': response.data
        }

    return response


# for views 
class CustomViewErrorSerializer(serializers.Serializer):
    message = serializers.CharField()
    errors = serializers.ListField(child=serializers.DictField())    

# for djoser
# def custom_exception_handler_djoser(exc, context):
#     response = exception_handler(exc, context)
#     if isinstance(exc, djoser_exceptions):
#         # Custom error message for "No active account found" error
#         # if isinstance(exc, djoser_exceptions.ActivationError):
#         #     response.data = {'error': 'Invalid activation link'}
#         # elif isinstance(exc, djoser_exceptions.UserNotFound):
#         #     response.data = {'error': 'No user found with the given credentials'}
#         # elif isinstance(exc, djoser_exceptions.InvalidPassword):
#         #     response.data = {'error': 'Incorrect password'}
#         response.data = {
#             'message': 'Validation failed',
#             'errors': response.data
#         }

    # return response

