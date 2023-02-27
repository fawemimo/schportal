from rest_framework import serializers
from api.emails import (
    send_financial_aid_email,
    send_inquiries_email,
    send_interested_email,
    send_kids_coding_email,
    send_short_quizze_email,
    send_virtualclass_email,
)
from .models import *
from djoser.serializers import (
    UserCreateSerializer as BaseUserCreateSerializer,
    UserSerializer as BaseUserSerializer,
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data["id"] = self.user.id
        data["username"] = self.user.username
        data["first_name"] = self.user.first_name
        data["last_name"] = self.user.last_name
        data["student_id"] = self.user.student.student_idcard_id

        return data

    def validate_username(self, value):
        if not User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username does not exist")
        return value

    def validate_password(self, value):
        if not User.objects.filter(password=value).exists():
            raise serializers.ValidationError(
                "Incorrect password, Please enter a valid password"
            )
        return value


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ["id", "title", "child_1", "child_2"]


class AddCourseSerializer(serializers.ModelSerializer):
    coursecategory_id = serializers.IntegerField()

    class Meta:
        model = Course
        fields = [
            "id",
            "card_title",
            "title",
            "description",
            "course_code",
            "tech_subs",
            "audience",
            "coursecategory_id",
        ]

    def validate_coursecategory_id(self, value):
        if not CourseCategory.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Invalid Course Category ID supplied")
        return value

    def create(self, validated_data):
        course = Course(**validated_data)
        course.save()
        return course


class CourseSerializer(serializers.ModelSerializer):
    coursecategory = CourseCategorySerializer(read_only=True)

    class Meta:
        model = Course
        fields = "__all__"
        lookup_field = "slug"


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Student
        fields = [
            "id",
            "user",
            "student_idcard_id",
            "mobile_numbers",
            "profile_pic",
            "residential_address",
            "contact_address",
            "next_of_kin_fullname",
            "next_of_kin_contact_address",
        ]


class ScheduleSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    teacher = serializers.StringRelatedField()
    fee_dollar = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = [
            "id",
            "program_type",
            "course",
            "registration_status",
            "teacher",
            "fee",
            "discounted_fee",
            "fee_dollar",
            "discounted_fee_dollar",
            "startdate",
            "duration",
            "timing",
        ]

    def get_fee_dollar(self, obj):
        return obj.fee_dollar


class AddScheduleSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField()
    teacher_id = serializers.IntegerField()

    class Meta:
        model = Schedule
        fields = [
            "id",
            "course_id",
            "teacher_id",
            "fee",
            "discounted_fee",
            "startdate",
            "duration",
            "timing",
        ]


class TopBarSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopBar
        fields = "__all__"


class MainBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainBanner
        fields = "__all__"


class SectionBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionBanner
        fields = "__all__"


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = "__all__"


class TechIconSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechIcon
        fields = "__all__"


class FeaturedProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeaturedProject
        fields = "__all__"


class ComponentDumpSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentDump
        fields = "__all__"


class NavLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavLink
        fields = "__all__"


class NavLinkItemSerializer(serializers.ModelSerializer):
    navlink = NavLinkSerializer()

    class Meta:
        model = NavLinkItem
        fields = ["id", "item", "item_url", "navlink"]


class AddNavLinkItemSerializer(serializers.ModelSerializer):
    # navlink_id = serializers.IntegerField()

    class Meta:
        model = NavLinkItem
        fields = ["id", "item", "item_url"]

    def create(self, validated_data):
        navlinkid = self.context["navlink_id"]
        return NavLinkItem.objects.create(navlink_id=navlinkid, **validated_data)


class ShortQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortQuiz
        fields = "__all__"

    def create(self, validated_data):
        shortquiz = ShortQuiz(**validated_data)
        shortquiz.save()
        return shortquiz

    def save(self, **kwargs):
        fullname = self.validated_data["fullname"]
        email = self.validated_data["email"]
        mobile = self.validated_data["mobile"]
        tartiary_education = self.validated_data["tartiary_education"]
        tartiary_studied = self.validated_data["tartiary_studied"]
        secondary_sch = self.validated_data["secondary_sch"]
        secondary_studied = self.validated_data["secondary_studied"]
        tech_interest = self.validated_data["tech_interest"]
        more_about_you = self.validated_data["more_about_you"]

        shortquiz = ShortQuiz.objects.create(
            fullname=fullname,
            email=email,
            mobile=mobile,
            tartiary_education=tartiary_education,
            tartiary_studied=tartiary_studied,
            secondary_sch=secondary_sch,
            secondary_studied=secondary_studied,
            tech_interest=tech_interest,
            more_about_you=more_about_you,
        )

        send_short_quizze_email(
            fullname,
            email,
            mobile,
            tartiary_education,
            tartiary_studied,
            secondary_sch,
            secondary_studied,
            tech_interest,
            more_about_you,
        )

        return shortquiz


class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = "__all__"

    def save(self, **kwargs):
        fullname = self.validated_data["fullname"]
        email = self.validated_data["email"]
        mobile = self.validated_data["mobile"]
        message = self.validated_data["message"]

        inquiry = Inquiry.objects.create(
            fullname=fullname, email=email, mobile=mobile, message=message
        )

        send_inquiries_email(fullname, email, mobile, message)
        return inquiry


class InterestedFormSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField()

    class Meta:
        model = InterestedForm
        fields = ["id", "course_id", "full_name", "email", "mobile"]

    def validate_course_id(self, value):
        if not Course.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Course ID does not exist")
        return value

    def save(self, **kwargs):
        course_id = self.validated_data["course_id"]
        full_name = self.validated_data["full_name"]
        email = self.validated_data["email"]
        mobile = self.validated_data["mobile"]

        interestform = InterestedForm.objects.create(
            course_id=course_id, full_name=full_name, email=email, mobile=mobile
        )

        send_interested_email(course_id, full_name, email, mobile)
        return interestform


class EnrollBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ("id", "title", "start_date", "end_date")


class EnrollStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = (
            "student_idcard_id",
            "mobile_numbers",
            "profile_pic",
        )


class EnrollCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "title")


class EnrollmentSerializer(serializers.ModelSerializer):
    student = EnrollStudentSerializer(read_only=True)
    course = EnrollCourseSerializer(read_only=True)
    batch = EnrollBatchSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ["id", "student", "course", "batch", "enrolled", "training_date"]


class AssignmentSerializer(serializers.ModelSerializer):
    batch = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Assignment
        fields = ("id", "batch", "name", "assignment_file", "date_posted")


class AssignmentAllocationSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    assignment = AssignmentSerializer(read_only=True)
    supervisor = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = AssignmentAllocation
        fields = ["id", "student", "assignment", "supervisor", "start_date", "deadline"]


class ResourceSerializer(serializers.ModelSerializer):
    resource_type = serializers.StringRelatedField(read_only=True)
    slug = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Resource
        fields = (
            "id",
            "resource_type",
            "slug",
            "short_description",
            "primer",
            "cheat_sheat",
            "published",
        )
        lookup_field = "slug"

    def get_slug(self, obj):
        return obj.resource_type.slug


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "project_docs", "date_posted"]


class ProjectAllocationSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    project = ProjectSerializer()
    supervisor = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ProjectAllocation
        fields = [
            "id",
            "student",
            "project",
            "supervisor",
            "start_date",
            "delivery_status",
        ]


class CourseManualSerializer(serializers.ModelSerializer):
    course = EnrollCourseSerializer(many=True, read_only=True)

    class Meta:
        model = CourseManual
        fields = ["id", "title", "course", "manual", "date_posted"]


class CourseManualAllocationSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    course_manual = CourseManualSerializer()
    released_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = CourseManualAllocation
        fields = ["id", "student", "course_manual", "released_by", "when_released"]


class AddCourseCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"

    def create(self, validated_data):
        coursecard = Course(**validated_data)
        coursecard.save()
        return coursecard


class CourseCardSerializer(serializers.ModelSerializer):
    the_url = serializers.SerializerMethodField(read_only=True)
    fee = serializers.SerializerMethodField(source="schedule_set")
    discounted_fee = serializers.SerializerMethodField(source="schedule_set")
    fee_dollar = serializers.SerializerMethodField(source="schedule_set")
    discounted_fee_dollar = serializers.SerializerMethodField(source="schedule_set")
    program_type = serializers.SerializerMethodField(source="schedule_set")

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "card_title",
            "course_code",
            "is_virtual_class",
            "the_url",
            "fee",
            "discounted_fee",
            "fee_dollar",
            "discounted_fee_dollar",
            "card_thumb",
            "program_type",
            "audience",
            "audience_description",
            "frontpage_featured",
            "published",
            "slug",
            "location_state",
            "location_state_area",
        ]

        lookup_field = "slug"

    def get_the_url(self, obj):
        return f"{obj.location_state}/{obj.location_state_area}/{obj.slug}"

    def get_fee(self, obj):
        return obj.schedule_set.values("fee").first()

    def get_discounted_fee(self, obj):
        return obj.schedule_set.values("discounted_fee").first()

    def get_fee_dollar(self, obj):
        return obj.schedule_set.values("fee_dollar").first()

    def get_program_type(self, obj):
        return obj.schedule_set.values("program_type").first()

    def get_discounted_fee_dollar(self, obj):
        return obj.schedule_set.values("discounted_fee_dollar").first()


class StudentAttendanceSerializer(serializers.ModelSerializer):
    batch = serializers.StringRelatedField()
    student = serializers.StringRelatedField()

    class Meta:
        model = StudentAttendance
        fields = [
            "id",
            "student",
            "batch",
            "attendance_status",
            "timestamp",
            "attendance_comment",
            "raise_warning",
        ]


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ["id", "username", "email", "password", "first_name", "last_name"]


class UserSerializer(BaseUserSerializer):
    student = StudentSerializer(read_only=True)

    class Meta(BaseUserSerializer.Meta):
        fields = ["id", "username", "email", "first_name", "last_name", "student"]


class VirtualClassSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField()

    class Meta:
        model = VirtualClass
        fields = [
            "id",
            "country_of_residence",
            "course_id",
            "full_name",
            "email",
            "mobile",
            "remarks",
        ]

    def create(self, validated_data):
        virtualclass = VirtualClass(**validated_data)
        virtualclass.save()
        return virtualclass

    def validate_course(self, value):
        if not Course.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Invalid Course ID supplied")
        return value

    def save(self, **kwargs):
        course_id = self.validated_data["course_id"]
        full_name = self.validated_data["full_name"]
        email = self.validated_data["email"]
        mobile = self.validated_data["mobile"]
        remarks = self.validated_data["remarks"]
        country_of_residence = self.validated_data["country_of_residence"]

        virtualclass = VirtualClass.objects.create(
            course_id=course_id,
            full_name=full_name,
            email=email,
            mobile=mobile,
            remarks=remarks,
            country_of_residence=country_of_residence,
        )

        send_virtualclass_email(
            course_id, full_name, email, mobile, remarks, country_of_residence
        )
        return virtualclass


class KidsCodingSerializer(serializers.ModelSerializer):
    class Meta:
        model = KidsCoding
        fields = (
            "full_name",
            "email",
            "mobile",
            "age_bracket",
            "remarks",
        )

    def create(self, validated_data):
        kidscoding = KidsCoding(**validated_data)
        kidscoding.save()
        return kidscoding

    def save(self, **kwargs):
        full_name = self.validated_data["full_name"]
        email = self.validated_data["email"]
        mobile = self.validated_data["mobile"]
        age_bracket = self.validated_data["age_bracket"]
        remarks = self.validated_data["remarks"]

        kidscoding = KidsCoding.objects.create(
            full_name=full_name,
            email=email,
            mobile=mobile,
            age_bracket=age_bracket,
            remarks=remarks,
        )

        send_kids_coding_email(age_bracket, full_name, email, mobile, remarks)

        return kidscoding


class KidsCodingCourseSerializer(serializers.ModelSerializer):
    coursecategory = CourseCategorySerializer(read_only=True)
    the_url = serializers.SerializerMethodField(read_only=True)
    fee = serializers.SerializerMethodField(source="schedule_set")
    discounted_fee = serializers.SerializerMethodField(source="schedule_set")

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "coursecategory",
            "card_title",
            "course_code",
            "the_url",
            "fee",
            "discounted_fee",
            "card_thumb",
            "audience",
            "audience_description",
            "frontpage_featured",
            "published",
            "slug",
            "location_state",
            "location_state_area",
        ]

    def get_the_url(self, obj):
        return f"{obj.location_state}/{obj.location_state_area}/{obj.slug}"

    def get_fee(self, obj):
        return obj.schedule_set.only("id").values("fee").first()

    def get_discounted_fee(self, obj):
        return obj.schedule_set.only("id").values("discounted_fee").first()


class CourseOutlineSerializer(serializers.ModelSerializer):
    pdf = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "pdf",
            "ordering",
            "frontpage_featured",
            "published",
            "delisted",
            "slug",
            "course_code",
            "location_state",
            "location_state_area",
            "card_title",
        ]

        lookup_field = "slug"

    def get_pdf(self, obj):
        return f"{obj.course_outline_pdf.url}"


class InternationalModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternationalModel
        fields = [
            "id",
            "country_name",
            "flag",
            "country_code",
            "topbar_src",
            "intro_txt",
        ]

    lookup_field = "country_name"


class AlumiConnectSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlumiConnect
        fields = ["id", "first_name", "last_name", "title", "date_posted"]

    def create(self, validated_data):
        alumiconnect = AlumiConnect(**validated_data)
        alumiconnect.save()
        return alumiconnect


class CommunityConnectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityConnect
        fields = [
            "id",
            "completed",
            "community",
            "title",
            "descriptions",
            "image",
            "start_date",
        ]


class FinancialAidSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialAid
        fields = [
            "id",
            "aid_type",
            "first_name",
            "last_name",
            "email",
            "mobile",
            "date_posted",
        ]

    def create(self, validated_data):
        financialaid = FinancialAid(**validated_data)
        financialaid.save()
        return financialaid

    def save(self, **kwargs):
        aid_type = self.validated_data["aid_type"]
        first_name = self.validated_data["first_name"]
        last_name = self.validated_data["last_name"]
        email = self.validated_data["email"]
        mobile = self.validated_data["mobile"]

        financial_aid = FinancialAid.objects.create(
            aid_type=aid_type,
            first_name=first_name,
            last_name=last_name,
            email=email,
            mobile=mobile,
        )

        send_financial_aid_email(aid_type, first_name, last_name, email, mobile)

        return financial_aid


class TermsOfServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsOfService
        fields = ["id", "title", "descriptions", "date_created"]


class VirtualVsOthersSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualVsOther
        fields = ["id", "title", "descriptions"]


class HowItWorksSerializer(serializers.ModelSerializer):
    class Meta:
        model = HowItWork
        fields = ["id", "how_it_work_class","content"]
