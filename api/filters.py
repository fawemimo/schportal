from django_filters.rest_framework import FilterSet
from .models import *


class JobFilter(FilterSet):
    class Meta:
        model = Job
        fields = {
            'job_category_id':['exact'],
            'job_category__experience':['exact'],
            'job_category__job_type':['exact'],
            'job_category__job_location':['exact']
        }

class EmployerFilterSet(FilterSet):
    pass
    # class Meta:
    #     model = Student
    #     fields = {
    #         ''
    #     }        