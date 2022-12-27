from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from .models import *
from .serializers import *

# Create your views here.


class CourseCategoryViewSet(viewsets.ModelViewSet):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer
    permission_classes = []


class CourseViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'patch', 'post', 'delete']
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return AddCourseSerializer
        return CourseSerializer
    permission_classes = []


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = []


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = []


class ScheduleViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = ScheduleSerializer

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return AddScheduleSerializer
        return ScheduleSerializer

    def get_queryset(self):
        return Schedule.objects.filter(course_id=self.kwargs['course_pk']).all()

    permission_classes = []


class TopBarViewSet(viewsets.ModelViewSet):
    queryset = TopBar.objects.all()
    serializer_class = TopBarSerializer
    permission_classes = []


class MainBannerViewSet(ModelViewSet):
    queryset = MainBanner.objects.all()
    serializer_class = MainBannerSerializer
    permission_classes = []


class SectionBannerViewSet(viewsets.ModelViewSet):
    queryset = SectionBanner.objects.all()
    serializer_class = SectionBannerSerializer
    permission_classes = []


class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = []


class TechIconViewSet(viewsets.ModelViewSet):
    queryset = TechIcon.objects.all()
    serializer_class = TechIconSerializer
    permission_classes = []


class FeaturedProjectViewSet(viewsets.ModelViewSet):
    queryset = FeaturedProject.objects.all()
    serializer_class = FeaturedProjectSerializer
    permission_classes = []


class ComponentDumpViewSet(viewsets.ModelViewSet):
    queryset = ComponentDump.objects.all()
    serializer_class = ComponentDumpSerializer
    permission_classes = []
