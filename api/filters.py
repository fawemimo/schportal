from django.db.models import Q
from django_filters import filters as filtering
from django_filters.rest_framework import FilterSet

from .models import *


class JobFilter(FilterSet):
    experience = filtering.CharFilter(method="filter_by_experience")
    job_type = filtering.CharFilter(method="filter_by_job_type")
    job_location = filtering.CharFilter(method="filter_by_job_location")
    job_category = filtering.CharFilter(method="filter_by_job_category")
    class Meta:
        model = Job
        fields = ["experience", "job_type", "job_location","job_category"]

    @classmethod
    def filter_by_job_location(cls, queryset, name, value):
        names = value.strip().split(",")
        return queryset.filter(Q(job_location__in=names))

    @classmethod
    def filter_by_job_type(cls, queryset, name, value):
        names = value.strip().split(",")
        return queryset.filter(Q(job_type__in=names))

    @classmethod
    def filter_by_experience(cls, queryset, name, value):
        names = value.strip().split(",")
        return queryset.filter(Q(experience__title__in=names))

    @classmethod
    def filter_by_job_category(cls,queryset, name, value):
        names = value.strip().split(",")        
        return queryset.filter(Q(job_category__title__in=names))


class EmployerFilterSet(FilterSet):
    pass
    # class Meta:
    #     model = Student
    #     fields = {
    #         ''
    #     }
