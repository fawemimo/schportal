from datetime import datetime

from decouple import config
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import filters, parsers, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from api.models import *
from api.pdf import *

from .filters import *
from .models import *
from .paginations import *
from .permissions import *
from .serializers import *
from .emails import *


class UserViewSet(DjoserUserViewSet):
    # serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = self.get_queryset().get(pk=response.data['id'])
        email = user.email
        message = 'Thank you for registering with us!'
        send_employer_sign_up_email(email)
        return response

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer


class CourseCategoryViewSet(ModelViewSet):
    serializer_class = CourseCategorySerializer
    permission_classes = []

    def get_queryset(self):
        return CourseCategory.objects.prefetch_related("course_set")


class CourseViewSet(ModelViewSet):
    http_method_names = ["get", "patch", "post", "delete"]
    serializer_class = CourseSerializer
    lookup_field = "slug"
    lookup_value_regex = "[^/]+"

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return AddCourseSerializer
        return CourseSerializer

    def get_queryset(self):
        return Course.objects.order_by("ordering").select_related("coursecategory")


class AnnouncementViewSet(ModelViewSet):
    serializer_class = AnnouncementSerializer

    def get_queryset(self):
        now = datetime.now()
        return Announcement.objects.filter(is_published=True).exclude(
            expiration_date__date__lte=now, expiration_date__time__lte=now
        )


class CareerSectionViewSet(ModelViewSet):
    http_method_names = ["get"]
    serializer_class = CareerSectionSerializer
    queryset = CareerSection.objects.all()


class CareerApplicantViewSet(ModelViewSet):
    http_method_names = ["get", "post"]
    serializer_class = CareerApplicantSerializer
    queryset = CareerApplicant.objects.select_related("career_opening")


class CareerCategoryViewSet(ModelViewSet):
    htto_method_names = ["get"]
    serializer_class = CareerCategorySerializer
    queryset = CareerCategory.objects.prefetch_related("careeropening_set")


class AlbumSectionViewSet(ModelViewSet):
    http_method_names = ["get"]
    serializer_class = AlbumSectionSerializer
    queryset = AlbumSection.objects.all()


class AlumiConnectSectionViewSet(ModelViewSet):
    http_method_names = ["get"]
    serializer_class = AlumiConnectSectionSerailizer
    queryset = AlumiConnectSection.objects.all()


class ScholarshipSectionViewSet(ModelViewSet):
    http_method_names = ["get"]
    serializer_class = ScholarshipSectionSerializer
    queryset = ScholarshipSection.objects.all()


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAdminUser]


class StudentViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "head", "options", "put"]

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return UpdateStudentSerializer
        return StudentSerializer

    def get_queryset(self):
        if self.request.user.user_type == "student":
            return Student.objects.filter(user_id=self.request.user.id).select_related(
                "user"
            )

    def get_permissions(self):
        if self.request.method in ["POST", "PATCH", "GET", "PUT"]:
            return [IsStudentType()]
        return [permissions.IsAdminUser()]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        date_of_birth = request.data.get("date_of_birth", None)
        mobile_numbers = request.data.get("mobile_numbers", None)
        residential_address = request.data.get("residential_address", None)
        contact_address = request.data.get("contact_address", None)
        next_of_kin_fullname = request.data.get("next_of_kin_fullname", None)
        next_of_kin_contact_address = request.data.get(
            "next_of_kin_contact_address", None
        )
        next_of_kin_mobile_number = request.data.get("next_of_kin_mobile_number", None)
        relationship_with_next_kin = request.data.get(
            "relationship_with_next_kin", None
        )
        cv_upload = request.data.get("cv_upload", None)
        profile_pic = request.data.get("profile_pic", None)

        if profile_pic:
            setattr(instance, "profile_pic", profile_pic)

        if cv_upload:
            setattr(instance, "cv_upload", cv_upload)

        if date_of_birth:
            setattr(instance, "date_of_birth", date_of_birth)

        if mobile_numbers:
            setattr(instance, "mobile_numbers", mobile_numbers)

        if residential_address:
            setattr(instance, "residential_address", residential_address)

        if contact_address:
            setattr(instance, "contact_address", contact_address)

        if next_of_kin_contact_address:
            setattr(
                instance, "next_of_kin_contact_address", next_of_kin_contact_address
            )

        if next_of_kin_mobile_number:
            setattr(instance, "next_of_kin_mobile_number", next_of_kin_mobile_number)

        if relationship_with_next_kin:
            setattr(instance, "relationship_with_next_kin", relationship_with_next_kin)

        if next_of_kin_fullname:
            setattr(instance, "next_of_kin_fullname", next_of_kin_fullname)

        instance.save()
        serializer = UpdateStudentSerializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def payments_secret(self, request):
        #  squad authoriztion key
        request = {"Authorization": config("SQUAD_SECRET_KEY")}
        return Response(request, status=status.HTTP_200_OK)


class StudentUpdateViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "head", "options"]

    permission_classes = [IsStudentType]
    serializer_class = StudentSerializer

    def get_queryset(self):
        return Student.objects.filter(user_id=self.request.user.id).select_related(
            "user"
        )

    @action(
        detail=False,
        methods=["GET", "POST", "PATCH"],
        permission_classes=[IsStudentType],
        serializer_class=UpdateProfilePicSerializer,
    )
    def profile(self, request):
        student = Student.objects.get(user=self.request.user.id)

        serializer = UpdateProfilePicSerializer(student)

        if request.method == "GET":
            serializer = UpdateProfilePicSerializer(student)
            return Response(serializer.data)

        elif request.method == "POST":
            serializer = UpdateProfilePicSerializer(student, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["GET", "POST", "PATCH"],
        permission_classes=[IsStudentType],
        serializer_class=UploadCvSerializer,
    )
    def cv(self, request):
        student = Student.objects.get(user=self.request.user.id)

        serializer = UploadCvSerializer(student)

        if request.method == "GET":
            serializer = UploadCvSerializer(student)
            return Response(serializer.data)

        elif request.method == "POST":
            serializer = UploadCvSerializer(student, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScheduleViewSet(ModelViewSet):
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
            .select_related("course")
        )

    permission_classes = []


class TopBarViewSet(ModelViewSet):
    queryset = TopBar.objects.all()
    serializer_class = TopBarSerializer
    permission_classes = []


class MainBannerViewSet(ModelViewSet):
    queryset = MainBanner.objects.filter(published=True).order_by("ordering").all()
    serializer_class = MainBannerSerializer
    permission_classes = []


class SectionBannerViewSet(ModelViewSet):
    queryset = SectionBanner.objects.all()
    serializer_class = SectionBannerSerializer
    permission_classes = []


class TestimonialViewSet(ModelViewSet):
    queryset = Testimonial.objects.filter(published=True).all()
    serializer_class = TestimonialSerializer
    permission_classes = []


class TechIconViewSet(ModelViewSet):
    queryset = TechIcon.objects.filter(published=True)
    serializer_class = TechIconSerializer
    permission_classes = []


class FeaturedProjectViewSet(ModelViewSet):
    queryset = FeaturedProject.objects.all()
    serializer_class = FeaturedProjectSerializer
    permission_classes = []


class ComponentDumpViewSet(ModelViewSet):
    queryset = ComponentDump.objects.all()
    serializer_class = ComponentDumpSerializer
    permission_classes = []


class NavLinkViewSet(ModelViewSet):
    queryset = NavLink.objects.all()
    serializer_class = NavLinkSerializer
    permission_classes = []


class AboutUsSectionViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = AboutUsSection.objects.all()
    serializer_class = AboutUsSectionSerializer


class StudentLoanSectionViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = StudentLoanSection.objects.all()
    serializer_class = StudentLoanSectionSerializer


class NavLinkItemViewSet(ModelViewSet):
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


class ShortQuizViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    queryset = ShortQuiz.objects.all()
    serializer_class = ShortQuizSerializer
    permission_classes = []


class InquiryViewSet(ModelViewSet):
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


class EnrollmentViewSet(ModelViewSet):
    http_method_names = ["post", "get", "patch"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return EnrollmentSerializer
        return EnrollmentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def get_serializer_context(self):
        return {"course_id": self.kwargs.get("course_pk")}

    def get_queryset(self):
        return Enrollment.objects.filter(
            course_id=self.kwargs.get("course_id")
        ).select_related("course")


class AssignmentViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch"]

    serializer_class = AssignmentBatchSerializer
    permission_classes = [IsStudentType]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Batch.objects.prefetch_related("assignmentallocation_set")
        return Batch.objects.filter(students__user=self.request.user).prefetch_related(
            "assignmentallocation_set"
        )


class ProjectViewSet(ModelViewSet):
    http_method_names = ["get"]

    serializer_class = ProjectAllocationSerializer
    permission_classes = [IsStudentType]

    def get_queryset(self):
        if self.request.user.is_staff:
            return ProjectAllocation.objects.all()
        return (
            ProjectAllocation.objects.filter(student__user_id=self.request.user.id)
            .filter(project__project_assigned=True)
            .select_related("student", "project", "supervisor")
        )


class CourseCardViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    queryset = (
        Course.objects.filter(published=True)
        .filter(kids_coding=False)
        .order_by("ordering")
        .select_related("coursecategory")
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


class CoursesViewSet(ModelViewSet):
    http_method_names = ["get"]

    def get_queryset(self):
        return Course.objects.filter(
            enrollment__student__user_id=self.request.user.id
        ).select_related("coursecategory")

    serializer_class = EnrollCourseSerializer
    permission_classes = [IsStudentType]


class CourseManualViewSet(ModelViewSet):
    http_method_names = ["get"]

    serializer_class = BatchSerializer
    permission_classes = [IsStudentType]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Batch.objects.all()
        elif self.request.user.is_active:
            return (
                Batch.objects.filter(students__user=self.request.user)
                .prefetch_related("course_manuals")
                .select_related("course")
            )
        else:
            pass


class ResourceViewSet(ModelViewSet):
    http_method_names = ["get"]

    queryset = Resource.objects.filter(published=True).select_related("resource_type")
    serializer_class = ResourceSerializer
    permission_classes = []

    lookup_field = "resource_type__slug"
    lookup_value_regex = "[^/]+"


class StudentAttendanceViewSet(ModelViewSet):
    http_method_names = ["get"]

    serializer_class = StudentAttendanceSerializer
    permission_classes = [IsStudentType]

    def get_queryset(self):
        if self.request.user.is_active:
            return (
                StudentAttendance.objects.filter(student__user_id=self.request.user.id)
                .select_related("student")
                .select_related("batch")
            )


class CourseHomepageFeatured(ModelViewSet):
    http_method_names = ["get"]

    queryset = (
        Course.objects.order_by("ordering")
        .filter(frontpage_featured=True)
        .filter(published=True)
        .select_related("coursecategory")
    )
    serializer_class = CourseCardSerializer

    lookup_field = "slug"
    lookup_value_regex = "[^/]+"


class VirtualClassViewSet(ModelViewSet):
    http_method_names = ["get", "post"]

    queryset = VirtualClass.objects.select_related("course")
    serializer_class = VirtualClassSerializer


class KidsCodingViewSet(ModelViewSet):
    http_method_names = ["get", "post"]

    queryset = KidsCoding.objects.all()
    serializer_class = KidsCodingSerializer


class KidsCodingCourseViewSet(ModelViewSet):
    http_method_names = ["get"]

    serializer_class = KidsCodingCourseSerializer

    def get_queryset(self):
        return (
            Course.objects.filter(kids_coding=True)
            .filter(published=True)
            .order_by("ordering")
            .select_related("coursecategory")
        )


class CourseDetailsViewSet(ModelViewSet):
    http_method_names = ["get"]

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
            .select_related("coursecategory")
        )


class CourseOutlineViewSet(ModelViewSet):
    http_method_names = ["get"]

    serializer_class = CourseOutlineSerializer
    lookup_field = "slug"
    lookup_value_regex = "[^/]+"

    def get_serializer_context(self):
        return {"slug": self.kwargs.get("slug")}

    def get_queryset(self):
        return Course.objects.filter(slug=self.kwargs.get("slug")).select_related(
            "coursecategory"
        )


class CourseDetailsFeaturedViewSet(ModelViewSet):
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
            .select_related("coursecategory")
        )


class KidCourseDetailsFeaturedViewSet(ModelViewSet):
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
            .select_related("coursecategory")
        )


class InternationalModelViewSet(ModelViewSet):
    http_method_names = ["get"]

    serializer_class = InternationalModelSerializer

    def get_queryset(self):
        return InternationalModel.objects.order_by("ordering").all()

    lookup_field = "country_name"
    lookup_value_regex = "[^/]+"


class FeaturedVirtualClassViewSet(ModelViewSet):
    http_method_names = ["get"]

    serializer_class = CourseCardSerializer
    lookup_field = "slug"
    lookup_value_regex = "[^/]+"

    def get_queryset(self):
        return (
            Course.objects.filter(is_virtual_class=True)
            .filter(published=True)
            .order_by("ordering")
            .select_related("coursecategory")
        )


class AlumiConnectViewSet(ModelViewSet):
    http_method_name = ["get", "post"]

    queryset = AlumiConnect.objects.all()
    serializer_class = AlumiConnectSerializer


class CommunityConnectViewSet(ModelViewSet):
    http_method_name = ["get"]

    queryset = CommunityConnect.objects.order_by("ordering")
    serializer_class = CommunityConnectSerializer


class FinancialAidViewSet(ModelViewSet):
    http_method_names = ["get", "post"]

    queryset = FinancialAid.objects.all()
    serializer_class = FinancialAidSerializer


class TermsOfServiceViewSet(ModelViewSet):
    http_method_names = ["get"]

    queryset = TermsOfService.objects.all()
    serializer_class = TermsOfServiceSerializer


class HowItWorksViewSet(ModelViewSet):
    http_method_names = ["get"]

    queryset = HowItWork.objects.all()
    serializer_class = HowItWorksSerializer


class VirtualVsOthersViewSet(ModelViewSet):
    http_method_names = ["get"]

    queryset = VirtualVsOther.objects.all()
    serializer_class = VirtualVsOthersSerializer


class OurTeamViewSet(ModelViewSet):
    http_method_names = ["get"]

    queryset = OurTeam.objects.order_by("?")
    serializer_class = OurTeamSerializer


class SponsorshipsViewSet(ModelViewSet):
    http_method_names = ["post"]

    queryset = Sponsor.objects.all()
    serializer_class = SponsorshipSerializer


class AlbumViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Album.objects.prefetch_related("albumdetail_set")
    serializer_class = AlbumSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = [
        "main_title",
        "event_date",
        "main_description",
        "albumdetail__title",
        "albumdetail__descriptions",
    ]
    pagination_class = BasePagination


# JobPortal region


class EmployerViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "head", "options", "put"]
    permission_classes = [IsEmployerType]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return EmployerSerializer
        elif self.request.method in ["POST", "PATCH","PUT"]:
            return UpdateEmployerSerializer
        else:
            return EmployerSerializer

    def get_queryset(self):
        if self.request.user.user_type == "employer":
            return Employer.objects.filter(user_id=self.request.user.id)

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        tagline = request.data.get("tagline", None)
        location = request.data.get("location", None)
        contact_person = request.data.get("contact_person", None)
        contact_address = request.data.get("contact_address", None)
        company_name = request.data.get("company_name", None)
        company_logo = request.data.get("company_logo", None)
        kyc_document = request.data.get("kyc_document", None)
        contact_person_mobile = request.data.get("contact_person_mobile", None)
        company_url = request.data.get("company_url", None)

        if kyc_document:
            setattr(instance,"kyc_document", kyc_document)

        if company_logo:
            setattr(instance, "company_logo", company_logo)

        if tagline:
            setattr(instance, "tagline", tagline)

        if location:
            setattr(instance, "location", location)

        if contact_person:
            setattr(instance, "contact_person", contact_person)

        if contact_address:
            setattr(instance, "contact_address", contact_address)

        if contact_person_mobile:
            setattr(instance, "contact_person_mobile", contact_person_mobile)

        if company_url:
            setattr(instance, "company_url", company_url)

        if company_name:
            setattr(instance, "company_name", company_name)

        instance.save()
        serializer = UpdateEmployerSerializer(instance)
        return Response(serializer.data)


class JobViewSet(ModelViewSet):
    http_method_names = ["get", "post", "delete", "patch", "put"]

    queryset = (
        Job.objects.filter(posting_approval=True)
        .exclude(close_job=True)
        .select_related("employer")
    )
    serializer_class = JobSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = JobFilter
    search_fields = [
        "job_title",
        "job_category__title",
        "employer__company_name",
        "experience__title",
    ]
    ordering_fields = ["date_posted", "date_updated"]
    pagination_class = BasePagination
    lookup_field = "slug"
    lookup_regex_values = "[^/]+"

    def get_permissions(self):
        if self.request.method in ["POST", "DELETE", "PATCH"]:
            return [IsEmployerType()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return JobSerializer
        elif self.request.method in ["POST", "DELETE"]:
            return PostJobSerializer
        elif self.request.method in ["PATCH", "PUT"]:
            return PatchJobSerializer

    def get_serializer_context(self):
        return {
            "employer_id": self.kwargs.get("employer_pk"),
            "job_category_id": self.kwargs.get("job_category_pk"),
            "experience_id": self.kwargs.get("experience_pk"),
        }

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(
            {"success": "Your Profile is Pending Approval. Contact the Admin"},
            status=201,
        )


class JobTypeViewSet(ModelViewSet):
    http_method_name = ["get"]
    serializer_class = JobTypeSerializer
    queryset = JobType.objects.all()


class JobLocationViewSet(ModelViewSet):
    http_method_name = ["get"]
    serializer_class = JobLocationSerializer
    queryset = JobLocation.objects.all()


class JobCategoryViewSet(ModelViewSet):
    http_method_name = ["get"]
    serializer_class = JobCategorySerializer
    queryset = JobCategory.objects.all()


class JobExperienceViewSet(ModelViewSet):
    http_method_name = ["get"]
    serializer_class = JobExperienceSerializer
    queryset = JobExperience.objects.all()


class EmployerJobApplicantViewSet(ModelViewSet):
    http_method_names = ["get"]

    serializer_class = EmployerPostedJobSerializer
    permission_classes = [IsEmployerType]
    pagination_class = BasePagination
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return Job.objects.filter(employer__user=self.request.user).select_related(
            "employer"
        )


class ApplicantsViewSet(ModelViewSet):
    http_method_names = ["get"]

    serializer_class = ApplicantsSerializer
    permission_classes = [IsEmployerType]
    pagination_class = BasePagination
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return JobApplication.objects.filter(
            job_id=self.kwargs.get("job_pk")
        ).select_related("job")


class StudentAppliedJobViewSet(ModelViewSet):
    http_method_names = ["get"]

    serializer_class = StudentJobApplicationSerializer
    permission_classes = [IsStudentType]
    pagination_class = BasePagination

    def get_queryset(self):
        return Student.objects.filter(user=self.request.user).prefetch_related(
            "jobapplication_set"
        )


class StudentApplicationForJobViewSet(ModelViewSet):
    http_method_names = ["post", "get"]

    def get_permissions(self):
        if self.request.user.user_type == "student":
            return [IsStudentType()]
        return Response({"error": "User is not a student"})

    def get_queryset(self):
        return JobApplication.objects.filter(
            student__user=self.request.user
        ).select_related("student", "job")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return JobApplicationSerializer
        return JobApplicationSerializer

    def get_serializer_context(self):
        return {"student_id": self.kwargs.get("student_pk")}

    def create(self, request, *args, **kwargs):
        serializer = JobApplicationSerializer(
            data=request.data, context={"user_id": self.request.user.id}
        )
        serializer.is_valid(raise_exception=True)
        post_job = serializer.save()
        serializer = JobApplicationSerializer(post_job)
        return Response(serializer.data)


# End JobPortal region


# Billing region


class BillingPaymentViewSet(ModelViewSet):
    http_method_names = ["post", "get"]
    permission_classes = [IsStudentType]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BillingSerializer
        elif self.request.method == "POST":
            return PostBillingSerializer

    def get_queryset(self):
        return (
            Billing.objects.filter(student__user=self.request.user)
            .prefetch_related("billingdetail_set", "billingextrapayment_set")
            .select_related("student")
        )

    def get_serializer_context(self):
        return {
            "student_id": self.kwargs.get("student_pk"),
            "course_id": self.kwargs.get("course_pk"),
        }

    # @method_decorator(cache_page(1*60))
    # def dispatch(self, request, *args, **kwargs):
    #    return super().dispatch(request, *args, **kwargs)


class BillingDetailsViewSet(ModelViewSet):
    http_method_names = ["get", "post"]

    serializer_class = BillingDetailSerializer
    permission_classes = [IsStudentType]

    def get_queryset(self):
        return (
            BillingDetail.objects.filter(billing__student__user=self.request.user)
            .select_related("billing")
            .order_by("-date_paid")
            .filter(billing_id=self.kwargs.get("billing_pk"))
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PostBillingDetailSerializer
        elif self.request.method == "GET":
            return BillingDetailSerializer

    def get_serializer_context(self):
        return {"billing_id": self.kwargs.get("billing_pk")}

    def create(self, request, *args, **kwargs):
        serializer = PostBillingDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    # @method_decorator(cache_page(1*60))
    # def dispatch(self, request, *args, **kwargs):
    #    return super().dispatch(request, *args, **kwargs)
    # True:individual
    # False:list view
    @action(
        detail=True,
        methods=["GET"],
        permission_classes=[IsStudentType],
    )
    def receipts(self, request, billing_pk=None, pk=None):
        return create_receipts(self, billing_pk, pk)


# End Billing region

# BLOG POST REGION


class BlogPostViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = BlogPost.objects.filter(status="published")
    serializer_class = BlogPostSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["blog_category__title", "title", "content"]
    ordering_fields = ["date_created", "date_updated"]
    pagination_class = BasePagination
    lookup_field = "slug"
    lookup_regex_values = "[^/]+"

    @method_decorator(cache_page(60 * 2))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# END BLOG POST REGION
