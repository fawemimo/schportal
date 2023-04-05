from django.db.models import Q
from django_filters import filters as filtering
from django_filters.rest_framework import FilterSet

from .models import *


class JobFilter(FilterSet):
    experience = filtering.CharFilter(method="filter_by_experience")
    job_type = filtering.CharFilter(method="filter_by_job_type")
    job_location = filtering.CharFilter(method="filter_by_job_location")

    class Meta:
        model = Job
        fields = ["experience", "job_type", "job_location"]

    def filter_by_job_location(self, queryset, name, value):
        names = value.strip().split(",")
        queryset = Job.objects.filter(Q(job_location__in=names))
        return queryset

    def filter_by_job_type(self, queryset, name, value):
        names = value.strip().split(",")
        queryset = Job.objects.filter(Q(job_type__in=names))
        return queryset

    def filter_by_experience(self, queryset, name, value):
        names = value.strip().split(",")
        queryset = Job.objects.filter(Q(experience__in=names))

        return queryset


class EmployerFilterSet(FilterSet):
    pass
    # class Meta:
    #     model = Student
    #     fields = {
    #         ''
    #     }
