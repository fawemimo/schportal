from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework import permissions  
from rest_framework.response import Response
from rest_framework.decorators import action
# Create your views here.


class CourseCategoryViewSet(viewsets.ModelViewSet):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer
    permission_classes = []


class CourseViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'patch', 'post', 'delete']
    queryset = Course.objects.order_by('ordering').all()
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
    queryset = Testimonial.objects.filter(published=True).all()
    serializer_class = TestimonialSerializer
    permission_classes = []


class TechIconViewSet(viewsets.ModelViewSet):
    queryset = TechIcon.objects.filter(published=True).all()
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


class NavLinkViewSet(viewsets.ModelViewSet):
    queryset = NavLink.objects.all()
    serializer_class = NavLinkSerializer
    permission_classes = []


class NavLinkItemViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return NavLinkItem.objects.filter(navlink_id=self.kwargs['navlink_pk']).all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return AddNavLinkItemSerializer
        return NavLinkItemSerializer

    def get_serializer_context(self):
        return {
            'navlink_id': self.kwargs['navlink_pk']
        }
    permission_classes = []


class ShortQuizViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    queryset = ShortQuiz.objects.all()
    serializer_class = ShortQuizSerializer
    permission_classes = []


class InquiryViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer
    permission_classes = []


class EnrollmentViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def get_permissions(self):
        if self.request.method in ['PATCH','POST','DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]    


class AssignmentViewSet(viewsets.ModelViewSet):
    http_method_names = ['get','post','patch','delete']

    serializer_class = AssignmentSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Assignment.objects.all()
        return Assignment.objects.filter(assignment_given=True)

    def get_permissions(self):
        if self.request.method in ['PATCH','POST','DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]    


class ProjectViewSet(viewsets.ModelViewSet):
    http_method_names = ['get','post','patch','delete']

    serializer_class = ProjectSerializer

    def get_serializer_context(self):
        return {'student_id': self.kwargs.get('student_pk')}

    def get_queryset(self):
        if self.request.user.is_staff:
            return Project.objects.all()
        return Project.objects.filter(student=self.kwargs.get('student_id')).filter(project_assigned=True)    
     
    def get_permissions(self):
        if self.request.method in ['POST','PATCH','DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]    


class CoursesViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']

    def get_queryset(self):
        return Course.objects.prefetch_related('coursemanual_set').all()

    serializer_class = EnrollCourseSerializer
    permission_classes = [permissions.IsAuthenticated]


class CourseManualViewSet(viewsets.ModelViewSet):
    http_method_names = ['get','post','patch','delete']

    queryset = CourseManual.objects.prefetch_related('course').all()
    serializer_class = CourseManualSerializer

    def get_permissions(self):
        if self.request.method in ['POST','PATCH','DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]   
    

class ResourceViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']

    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer       
    permission_classes = []
