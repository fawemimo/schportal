from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class CourseCategoryViewSet(viewsets.ModelViewSet):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer
    permission_classes = []


class CourseViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "patch", "post", "delete"]
    serializer_class = CourseSerializer
    lookup_field = "slug"
    lookup_value_regex = "[^/]+"

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return AddCourseSerializer
        return CourseSerializer

    permission_classes = []

    def get_queryset(self):
        return Course.objects.order_by("ordering").all()


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAdminUser]


class StudentViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]

    serializer_class = StudentSerializer
    permission_classes = []

    def get_queryset(self):
        if self.request.user.is_authenticated:
            print()
            return Student.objects.filter(user_id=self.request.user.id)

    # def get_permissions(self):
    #     if self.request.method in ['PATCH', 'POST', 'GET']:
    #         return [permissions.IsAuthenticated()]
    #     return [permissions.IsAdminUser()]


class ScheduleViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    serializer_class = ScheduleSerializer

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return AddScheduleSerializer
        return ScheduleSerializer

    def get_queryset(self):
        return (
            Schedule.objects.filter(course_id__slug=self.kwargs["course_slug"])
            .filter(active=True)
            .all()
        )

    permission_classes = []


class TopBarViewSet(viewsets.ModelViewSet):
    queryset = TopBar.objects.all()
    serializer_class = TopBarSerializer
    permission_classes = []


class MainBannerViewSet(ModelViewSet):
    queryset = MainBanner.objects.filter(published=True).order_by("ordering").all()
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
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        return NavLinkItem.objects.filter(navlink_id=self.kwargs["navlink_pk"]).all()

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return AddNavLinkItemSerializer
        return NavLinkItemSerializer

    def get_serializer_context(self):
        return {"navlink_id": self.kwargs["navlink_pk"]}

    permission_classes = []


class ShortQuizViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    queryset = ShortQuiz.objects.all()
    serializer_class = ShortQuizSerializer
    permission_classes = []


class InquiryViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch"]

    queryset = Inquiry.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return InquirySerializer
        return InquirySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)


class InterestedFormViewSet(viewsets.ModelViewSet):
    http_method_names = ["post", "get", "patch"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return InterestedFormSerializer
        return InterestedFormSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def get_serializer_context(self):
        return {"course_id": self.kwargs.get("course_pk")}

    def get_queryset(self):
        return InterestedForm.objects.filter(
            course_id=self.kwargs.get("course_id")
        ).select_related("course")


class EnrollmentViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def get_permissions(self):
        if self.request.method in ["PATCH", "POST", "DELETE"]:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class AssignmentViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    serializer_class = AssignmentAllocationSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return AssignmentAllocation.objects.all()
        return AssignmentAllocation.objects.filter(
            student__user_id=self.request.user.id
        ).filter(assignment__assignment_given=True)

    def get_permissions(self):
        if self.request.method in ["PATCH", "POST", "DELETE"]:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


class ProjectViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    serializer_class = ProjectAllocationSerializer

    def get_serializer_context(self):
        return {"student_id": self.kwargs.get("student_pk")}

    def get_queryset(self):
        if self.request.user.is_staff:
            return ProjectAllocation.objects.all()
        return ProjectAllocation.objects.filter(
            student__user_id=self.request.user.id
        ).filter(project__project_assigned=True)

    def get_permissions(self):
        if self.request.method in ["POST", "PATCH", "DELETE"]:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


class CourseCardViewSet(viewsets.ModelViewSet):

    http_method_names = ["get", "post", "patch", "delete"]

    queryset = (
        Course.objects.filter(published=True)
        .filter(kids_coding=False)
        .order_by("ordering")
    )
    lookup_field = "slug"
    lookup_value_regex = "[^/]+"

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CourseCardSerializer
        elif self.request.method == "POST":
            return AddCourseCardSerializer
        return CourseCardSerializer

    def get_serializer_context(self):
        return {"course_id": self.kwargs.get("course_pk")}

    def get_permissions(self):
        if self.request.method in ["POST", "DELETE", "PATCH"]:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class CoursesViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]

    def get_queryset(self):
        return Course.objects.filter(enrollment__student__user_id=self.request.user.id)

    serializer_class = EnrollCourseSerializer
    permission_classes = [permissions.IsAuthenticated]


class CourseManualViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    queryset = CourseManualAllocation.objects.select_related("course_manual").all()
    serializer_class = CourseManualAllocationSerializer

    def get_permissions(self):
        if self.request.method in ["POST", "PATCH", "DELETE"]:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return CourseManualAllocation.objects.select_related("course_manual").all()
        elif self.request.user.is_active:
            return CourseManualAllocation.objects.filter(
                student__user=self.request.user
            ).select_related("course_manual")
        else:
            pass


class ResourceViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]

    queryset = Resource.objects.filter(published=True)
    serializer_class = ResourceSerializer
    permission_classes = []

    lookup_field = "resource_type__slug"
    lookup_value_regex = "[^/]+"


class StudentAttendanceViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]

    serializer_class = StudentAttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_active:
            return StudentAttendance.objects.filter(
                student__user_id=self.request.user.id
            )


class CourseHomepageFeatured(viewsets.ModelViewSet):
    http_method_names = ["get"]

    queryset = (
        Course.objects.order_by("ordering")
        .filter(frontpage_featured=True)
        .filter(published=True)
    )
    serializer_class = CourseCardSerializer

    lookup_field = "slug"
    lookup_value_regex = "[^/]+"


class VirtualClassViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post"]

    queryset = VirtualClass.objects.all()
    serializer_class = VirtualClassSerializer


class KidsCodingViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post"]

    queryset = KidsCoding.objects.all()
    serializer_class = KidsCodingSerializer


class KidsCodingCourseViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]

    serializer_class = KidsCodingCourseSerializer

    def get_queryset(self):
        return (
            Course.objects.filter(kids_coding=True)
            .filter(published=True)
            .order_by("ordering")
        )


class CourseDetailsViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]

    queryset = Course.objects.all()
    serializer_class = CourseCardSerializer

    lookup_field = "slug"
    lookup_value_regex = "[^/]+"

    def get_serializer_context(self):
        return {"slug": self.kwargs.get("slug")}

    def get_queryset(self):
        return (
            Course.objects.order_by("ordering")
            .filter(frontpage_featured=True)
            .filter(published=True)
        )


class CourseOutlineViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]

    serializer_class = CourseOutlineSerializer
    lookup_field = "slug"
    lookup_value_regex = "[^/]+"

    def get_serializer_context(self):
        return {"slug": self.kwargs.get("slug")}

    def get_queryset(self):
        return Course.objects.filter(slug=self.kwargs.get("slug"))


class CourseDetailsFeaturedViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]
    serializer_class = CourseCardSerializer

    lookup_field = "slug"
    lookup_value_regex = "[^/]+"

    def get_queryset(self):
        slug = self.request.query_params.get("slug")
        return (
            Course.objects.order_by("ordering")
            .filter(published=True)
            .filter(kids_coding=False)
            .exclude(slug=slug)
        )


class KidCourseDetailsFeaturedViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]
    serializer_class = CourseCardSerializer

    lookup_field = "slug"
    lookup_value_regex = "[^/]+"

    def get_queryset(self):
        slug = self.request.query_params.get("slug")
        return (
            Course.objects.order_by("ordering")
            .filter(published=True)
            .filter(kids_coding=True)
            .exclude(slug=slug)
        )


class InternationalModelViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]

    serializer_class = InternationalModelSerializer

    def get_queryset(self):
        return InternationalModel.objects.order_by("ordering").all()

    lookup_field = "country_name"
    lookup_value_regex = "[^/]+"


class FeaturedVirtualClassViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]

    serializer_class = CourseCardSerializer
    lookup_field = "slug"
    lookup_value_regex = "[^/]+"

    def get_queryset(self):
        return (
            Course.objects.filter(is_virtual_class=True)
            .filter(published=True)
            .order_by("ordering")
        )


class AlumiConnectViewSet(viewsets.ModelViewSet):
    http_method_name = ["get", "post"]

    queryset = AlumiConnect.objects.all()
    serializer_class = AlumiConnectSerializer


class CommunityConnectViewSet(viewsets.ModelViewSet):
    http_method_name = ["get"]

    queryset = CommunityConnect.objects.order_by("ordering")
    serializer_class = CommunityConnectSerializer


class FinancialAidViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post"]

    queryset = FinancialAid.objects.all()
    serializer_class = FinancialAidSerializer


class TermsOfServiceViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]

    queryset = TermsOfService.objects.all()
    serializer_class = TermsOfServiceSerializer


class HowItWorksViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]

    queryset = HowItWork.objects.all()
    serializer_class = HowItWorksSerializer


class VirtualVsOthersViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]

    queryset = VirtualVsOther.objects.all()
    serializer_class = VirtualVsOthersSerializer


class OurTeamViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]

    queryset = OurTeam.objects.order_by('?')
    serializer_class = OurTeamSerializer