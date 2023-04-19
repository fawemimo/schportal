from django.db.models import *
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.text import slugify
from django.db import transaction
from django.db import IntegrityError
from api.emails import (
    send_financial_aid_email,
    send_inquiries_email,
    send_interested_email,
    send_kids_coding_email,
    send_short_quizze_email,
    send_sponsorship_email,
    send_virtualclass_email,
    send_employer_sign_up_email
)

from .models import *
import random


class BaseTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        return token


class UserTokenObtainPairSerializer(BaseTokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data["id"] = self.user.id
        data["username"] = self.user.username
        data["first_name"] = self.user.first_name
        data["last_name"] = self.user.last_name
        data["email"] = self.user.email
        data["user_type"] = self.user.user_type

        try:
            if self.user.user_type == "student":
                data["student_id"] = self.user.student.id
            elif self.user.user_type == "employer":
                data["employer_id"] = self.user.employer.id
            else:
                pass

        except Exception as e:
            print(e)
        return data

    def validate_user_type(self, value):
        if not User.objects.filter(user_type=value).exists():
            raise serializers.ValidationError("User type does not exist")
        return value


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "date_joined",
        ]


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
    email = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            "id",
            "email",
            "full_name",
            "student_idcard_id",
            "date_of_birth",
            "mobile_numbers",
            "profile_pic",
            "cv_upload",
            "residential_address",
            "contact_address",
            "next_of_kin_fullname",
            "next_of_kin_contact_address",
            "next_of_kin_mobile_number",
            "relationship_with_next_kin",
        ]

    def get_email(self, obj):
        return obj.user.email


class UpdateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            "date_of_birth",
            "mobile_numbers",
            "profile_pic",
            "cv_upload",
            "residential_address",
            "contact_address",
            "next_of_kin_fullname",
            "next_of_kin_contact_address",
            "next_of_kin_mobile_number",
            "relationship_with_next_kin",
        ]


class UpdateProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "profile_pic"]

    def update(self, instance, validated_data):
        instance.profile_pic = validated_data["profile_pic"]
        return super(UpdateProfilePicSerializer, self).update(instance, validated_data)


class UploadCvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "cv_upload"]

    def update(self, instance, validated_data):
        instance.cv_upload = validated_data["cv_upload"]
        return super(UploadCvSerializer, self).update(instance, validated_data)


class ScheduleSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    teacher = serializers.StringRelatedField()
    fee = serializers.SerializerMethodField()
    discount_fee = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = [
            "id",
            "program_type",
            "course",
            "registration_status",
            "teacher",
            "fee",
            "discount_fee",
            "startdate",
            "duration",
            "timing",
        ]

    def get_fee(self, obj):
        if obj.program_type == "Onsite":
            return obj.fee
        return obj.fee_dollar

    def get_discount_fee(self, obj):
        if obj.program_type == "Onsite":
            return obj.discounted_fee
        return obj.discounted_fee_dollar


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


class AboutUsSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUsSection
        fields = "__all__"


class StudentLoanSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentLoanSection
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


class CareerSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerSection
        fields = "__all__"


class CareerApplicantSerializer(serializers.ModelSerializer):
    career_opening_id = serializers.IntegerField()

    class Meta:
        model = CareerApplicant
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "mobile",
            "career_opening_id",
            "resume",
        ]

    def validate_career_opening_id(self, value):
        if not CareerOpening.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                "Career opening with the given ID does not exist."
            )
        return value

    def create(self, validated_data):
        career_opening_id = validated_data["career_opening_id"]
        return CareerApplicant.objects.create(
            career_opening_id=career_opening_id, **validated_data
        )

    def save(self, **kwargs):
        career_opening_id = self.validated_data["career_opening_id"]
        first_name = self.validated_data["first_name"]
        last_name = self.validated_data["last_name"]
        email = self.validated_data["email"]
        mobile = self.validated_data["mobile"]
        resume = self.validated_data["resume"]

        try:
            careerapplicant = CareerApplicant.objects.create(
                career_opening_id=career_opening_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                mobile=mobile,
                resume=resume,
            )
            careerapplicant.save()

            return careerapplicant

        except Exception as e:
            pass


class CareerCategorySerializer(serializers.ModelSerializer):
    career_opening = serializers.SerializerMethodField()

    class Meta:
        model = CareerCategory
        fields = ["id", "title", "description", "career_opening"]

    def get_career_opening(self, obj):
        return obj.careeropening_set.filter(career_category_id=obj.id).values(
            "title", "description", "job_location__title", "employment_type__title"
        )


class AlbumSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumSection
        fields = "__all__"


class AlumiConnectSectionSerailizer(serializers.ModelSerializer):
    class Meta:
        model = AlumiConnectSection
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


class EnrollmentSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField()
    schedule_id = serializers.IntegerField()

    class Meta:
        model = Enrollment
        fields = ["id", "course_id", "schedule_id", "full_name", "email", "mobile"]

    def validate_course_id(self, value):
        if not Course.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Course ID does not exist")
        return value

    def validate_schedule_id(self, value):
        if not Schedule.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Course ID does not exist")
        return value

    def save(self, **kwargs):
        course_id = self.validated_data["course_id"]
        schedule_id = self.validated_data["schedule_id"]
        full_name = self.validated_data["full_name"]
        email = self.validated_data["email"]
        mobile = self.validated_data["mobile"]
        course = Course.objects.get(id=course_id)

        schedule = Schedule.objects.get(id=schedule_id)

        interestform = Enrollment.objects.create(
            course_id=course_id,
            schedule_id=schedule_id,
            full_name=full_name,
            email=email,
            mobile=mobile,
            program_type=schedule.program_type,
            start_date=schedule.startdate,
            fee=schedule.fee,
            fee_dollar=schedule.fee_dollar,
        )

        send_interested_email(course_id, full_name, email, mobile, schedule_id)
        return interestform


class SponsorshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = [
            "id",
            "name_of_sponsor",
            "selection",
            "organization_name",
            "number_of_student",
            "email",
            "phone_number",
            "remarks",
            "date_created",
        ]

    def save(self, **kwargs):
        name_of_sponsor = self.validated_data["name_of_sponsor"]
        selection = self.validated_data["selection"]
        number_of_student = self.validated_data["number_of_student"]
        email = self.validated_data["email"]
        phone_number = self.validated_data["phone_number"]
        remarks = self.validated_data["remarks"]
        organization_name = self.validated_data["organization_name"]

        sponsorship = Sponsor.objects.create(
            name_of_sponsor=name_of_sponsor,
            selection=selection,
            number_of_student=number_of_student,
            email=email,
            phone_number=phone_number,
            remarks=remarks,
            organization_name=organization_name,
        )

        send_sponsorship_email(
            name_of_sponsor,
            selection,
            number_of_student,
            email,
            phone_number,
            remarks,
            organization_name,
        )

        return sponsorship


class BatchSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()

    class Meta:
        model = Batch
        fields = ["id", "program_type", "title", "course", "course_manuals"]

    def to_representation(self, instance):
        self.fields["course_manuals"] = CourseManualSerializer(many=True)
        return super().to_representation(instance)


class AssignmentBatchSerializer(serializers.ModelSerializer):
    assignment = serializers.SerializerMethodField()
    teacher = serializers.StringRelatedField()

    class Meta:
        model = Batch
        fields = ["id", "title", "teacher", "assignment"]

    def get_assignment(self, obj):
        return obj.assignmentallocation_set.values(
            "assignment__name",
            "assignment__assignment_file",
            "assignment__assignment_given",
            "assignment__date_posted",
        )


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


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ("id", "name", "assignment_file", "date_posted")


class AssignmentAllocationSerializer(serializers.ModelSerializer):
    batch = BatchSerializer(read_only=True, many=False)
    assignment = AssignmentSerializer(read_only=True)
    supervisor = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = AssignmentAllocation
        fields = ["id", "batch", "assignment", "supervisor", "start_date", "deadline"]


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
            "why_choose_virtual",
            "identify_our_virutal_courses",
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
            "course",
            "first_name",
            "last_name",
            "email",
            "mobile",
            "residential_address",
            "guarantor_full_name",
            "guarantor_residential_contact_address",
            "relationship_with_guarantor",
            "guarantor_mobile",
            "date_posted",
        ]

    def create(self, validated_data):
        financialaid = FinancialAid(**validated_data)
        financialaid.save()
        return financialaid

    def save(self, **kwargs):
        aid_type = self.validated_data["aid_type"]
        course = self.validated_data["course"]
        first_name = self.validated_data["first_name"]
        last_name = self.validated_data["last_name"]
        email = self.validated_data["email"]
        mobile = self.validated_data["mobile"]
        residential_address = self.validated_data["residential_address"]
        guarantor_full_name = self.validated_data["guarantor_full_name"]
        guarantor_residential_contact_address = self.validated_data[
            "guarantor_residential_contact_address"
        ]
        relationship_with_guarantor = self.validated_data["relationship_with_guarantor"]
        guarantor_mobile = self.validated_data["guarantor_mobile"]

        financial_aid = FinancialAid.objects.create(
            aid_type=aid_type,
            course=course,
            first_name=first_name,
            last_name=last_name,
            email=email,
            mobile=mobile,
            residential_address=residential_address,
            guarantor_full_name=guarantor_full_name,
            guarantor_residential_contact_address=guarantor_residential_contact_address,
            relationship_with_guarantor=relationship_with_guarantor,
            guarantor_mobile=guarantor_mobile,
        )

        send_financial_aid_email(
            aid_type,
            course,
            first_name,
            last_name,
            email,
            mobile,
            relationship_with_guarantor,
            residential_address,
            guarantor_full_name,
            guarantor_residential_contact_address,
            guarantor_mobile,
        )

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
        fields = ["id", "how_it_work_class", "content"]


class OurTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = OurTeam
        fields = ["id", "image", "full_name", "designation", "social_dump"]


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = [
            "id",
            "title",
            "announcement",
            "date_created",
            "expiration_date",
            "is_published",
        ]


class ScholarshipSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScholarshipSection
        fields = "__all__"


class AlbumSerializer(serializers.ModelSerializer):
    album_details = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = [
            "id",
            "main_title",
            "main_description",
            "image_cover",
            "event_date",
            "date_posted",
            "album_details",
        ]

    def get_album_details(self, obj):
        return obj.albumdetail_set.filter(album_id=obj.id).values(
            "title", "descriptions", "image", "date_created"
        )


# JobPortal region


class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = [
            "id",
            "user",
            "contact_person",
            "contact_person_mobile",
            "location",
            "company_name",
            "company_url",
            "tagline",
            "company_logo",
            "profile_approval",
            "kyc_document",
            "date_created",
            "date_updated",
        ]


class UpdateEmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = [
            "id",
            "tagline",
            "location",
            "contact_person",
            "company_name",
            "company_logo",
            "contact_person_mobile",
            "company_url",
        ]


class JobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobType
        fields = "__all__"


class JobLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobLocation
        fields = "__all__"


class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = "__all__"


class JobExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobExperience
        fields = "__all__"


class PostJobSerializer(serializers.ModelSerializer):
    employer_id = serializers.IntegerField()
    job_category = JobCategorySerializer(many=True)
    experience = JobExperienceSerializer(many=True)
    job_type_id = serializers.IntegerField()
    job_location_id = serializers.IntegerField()

    class Meta:
        model = Job
        fields = [
            "id",
            "employer_id",
            "job_category",
            "job_title",
            "job_location_id",
            "experience",
            "job_type_id",
            "close_job",
            "job_summary",
            "job_responsibilities",
        ]

    def create(self, validated_data):
        employer_id = validated_data["employer_id"]
        job_category = validated_data["job_category"]
        job_location_id = validated_data["job_location_id"]
        job_type_id = validated_data["job_type_id"]
        experience = validated_data["experience"]
        job = Job.objects.create(
            employer_id=employer_id,
            job_location_id=job_location_id,
            job_type_id=job_type_id,
            **validated_data,
        )

        for x in job_category:
            job_category = JobCategory.objects.filter(**x)
            job.job_category.set(job_category)

        for x in experience:
            experience = JobExperience.objects.filter(**x)

            job.experience.set(experience)

        return job

    def validate_employer_id(self, value):
        if not Employer.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                "Employer with the give ID does not exist"
            )
        return value

    def validate_job_type_id(self, value):
        if not JobType.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                "JobType with the given ID does not exist"
            )
        return value

    def validate_job_location_id(self, value):
        if not JobLocation.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                "JobLocation with the given ID does not exist"
            )
        return value

    def save(self, **kwargs):
        job_type_id = self.validated_data["job_type_id"]
        job_location_id = self.validated_data["job_location_id"]
        job_title = self.validated_data["job_title"]
        job_summary = self.validated_data["job_summary"]
        job_responsibilities = self.validated_data["job_responsibilities"]
        close_job = self.validated_data["close_job"]

        employer_id = self.validated_data["employer_id"]
        job_category = self.validated_data["job_category"]
        experience = self.validated_data["experience"]

        try:
            
            num = range(100, 1000)
            ran = random.choice(num)
            slug = f"{(slugify(job_title))}-{ran}"

            job = Job.objects.create(
                employer_id=employer_id,
                job_type_id=job_type_id,
                job_location_id=job_location_id,
                job_title=job_title,
                job_summary=job_summary,
                slug=slug,
                job_responsibilities=job_responsibilities,
                close_job=close_job,
            )

            for x in job_category:
                job_category, _ = JobCategory.objects.get_or_create(**x)
                job.job_category.add(job_category)

            for x in experience:
                experience, _ = JobExperience.objects.get_or_create(**x)

                job.experience.add(experience)

            job.save()
            return job

        except Exception as e:
            print(e)
          


class PatchJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ["close_job"]


class JobSerializer(serializers.ModelSerializer):
    employer = EmployerSerializer()
    job_type = serializers.StringRelatedField()
    job_location = serializers.StringRelatedField()

    class Meta:
        model = Job
        fields = "__all__"
        lookup_field = "slug"

    def to_representation(self, instance):
        self.fields["job_category"] = JobCategorySerializer(many=True)
        self.fields["experience"] = JobExperienceSerializer(many=True)
        return super().to_representation(instance)


class StudentJobApplicationSerializer(serializers.ModelSerializer):
    job_applied_for = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            "id",
            "user",
            "full_name",
            "date_of_birth",
            "mobile_numbers",
            "job_applied_for",
        ]

    def get_job_applied_for(self, obj):
        return obj.jobapplication_set.values(
            "job_id",
            "job__employer__company_name",
            "job__employer__company_logo",
            "job__job_category",
            "job__job_title",
            "job__job_location",
            "job__job_type",
            "job__date_posted",
            "date_applied",
        )


class EmployerPostedJobSerializer(serializers.ModelSerializer):
    # applicants = serializers.SerializerMethodField()
    total_applicants = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            "id",
            "employer",
            "job_category",
            "job_title",
            "job_summary",
            "job_responsibilities",
            "date_posted",
            "date_updated",
            # "applicants",
            "total_applicants",
        ]

    def get_total_applicants(self, obj):
        return obj.jobapplication_set.count()

    # def get_applicants(self, obj):
    #     return obj.jobapplication_set.values(
    #         "id",
    #         "student",
    #         "student__date_of_birth",
    #         "job",
    #         "student__cv_upload",
    #         "date_applied",
    #     )


class ApplicantsSerializer(serializers.ModelSerializer):
    cv = serializers.SerializerMethodField()
    student_name = serializers.SerializerMethodField()
    student_profile_pics = serializers.SerializerMethodField()
    job_title = serializers.SerializerMethodField()

    class Meta:
        model = JobApplication
        fields = "__all__"

    def get_cv(self, obj):
        if obj.student.cv_upload is None:
            return obj.student.cv_upload.url
        return obj.student.cv_upload.url

    def get_student_name(self, obj):
        return obj.student.full_name

    def get_student_profile_pics(self, obj):
        return obj.student.profile_pic.url

    def get_job_title(self, obj):
        return obj.job.job_title


class JobApplicationSerializer(serializers.ModelSerializer):
    job_id = serializers.IntegerField()
    student_id = serializers.IntegerField()

    class Meta:
        model = JobApplication
        fields = ["id", "student_id", "job_id"]
        validators = [
            UniqueTogetherValidator(
                queryset=JobApplication.objects.all(),
                fields=["student_id", "job_id"],
                message=("You already apply for this job"),
            )
        ]

    def validate_job_id(self, value):
        if not Job.objects.filter(pk=value).exists():
            raise serializers.ValidationError("The selected Job ID does not exist")
        return value

    def validate_student_id(self, value):
        if not Student.objects.filter(pk=value).exists():
            raise serializers.ValidationError("The selected Student ID does not exist")
        return value

    def create(self, validated_data):
        jobapplication = JobApplication(**validated_data)
        jobapplication.save()
        return jobapplication

    def save(self, **kwargs):
        student_id = self.validated_data["student_id"]
        job_id = self.validated_data["job_id"]

        # get the student obj
        student_obj = Student.objects.get(id=student_id)
        try:
            if student_obj.job_ready == True:
                jobapplication = JobApplication.objects.create(
                    student_id=student_id, job_id=job_id, applied=True
                )

                return jobapplication
            else:
                raise serializers.ValidationError("Student is not Job ready yet")
                # raise serializers.ValidationError({"message":'Student is not Job ready yet'})
        except Exception as e:
            raise serializers.ValidationError("Student is not Job ready yet")


# EndJobPortalRegion


# Billing Region


class PostBillingSerializer(serializers.ModelSerializer):
    student_id = serializers.IntegerField()
    course_id = serializers.IntegerField()

    class Meta:
        model = Billing
        fields = [
            "id",
            "payment_completion_status",
            "student_id",
            "course_id",
        ]

    def create(self, validated_data):
        student_id = self.context["student_id"]
        course_id = self.context["course_id"]

        return Billing.objects.create(
            student_id=student_id, course_id=course_id, **validated_data
        )

    def validate_student_id(self, value):
        if not Student.objects.filter(id=value).exists():
            raise serializers.ValidationError("Student ID does not exist")
        return value

    def validate_course_id(self, value):
        if not Course.objects.filter(id=value).exists():
            raise serializers.ValidationError("Course ID does not exist")
        return value

    def save(self, **kwargs):
        payment_completion_status = self.validated_data["payment_completion_status"]
        course_id = self.validated_data["course_id"]
        # total_amount_paid = self.validated_data["total_amount_paid"]
        # total_amount = self.validated_data["total_amount"]
        student_id = self.validated_data["student_id"]
        # student = Student.objects.get(id=student_id)
        try:
            billing = Billing.objects.create(
                student_id=student_id,
                course_id=course_id,
                # total_amount_paid=total_amount_paid,
                # total_amount=total_amount,
                # first_name=student.user.first_name,
                # last_name=student.user.last_name,
                # email=student.user.email,
                payment_completion_status=payment_completion_status,
            )
            billing.save()

            return billing
        except ValueError as e:
            return e


class BillingSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()
    grand_total_paid = serializers.SerializerMethodField()
    grand_outstanding = serializers.SerializerMethodField()
    extra_payment = serializers.SerializerMethodField()
    billingdetails = serializers.SerializerMethodField()

    class Meta:
        model = Billing
        fields = [
            "id",
            "student",
            "course_fee",
            "course_name",
            "start_date",
            "payment_completion_status",
            "grand_total_paid",
            "grand_outstanding",
            "billingdetails",
            "extra_payment",
        ]

    def get_extra_payment(self, obj):
        return obj.billingextrapayment_set.filter(billing_id=obj.id).values(
            "id",
            "item_name",
            "item_name_fee",
            "amount_paid",
            "date_created",
            "date_updated",
        )

    def get_billingdetails(self, obj):
        return obj.billingdetail_set.filter(billing_id=obj.id).values(
            "id", "course_fee", "amount_paid", "date_paid"
        )

    def get_grand_total_paid(self, obj):
        try:
            extrapayment = obj.billingextrapayment_set.filter(
                billing_id=obj.id
            ).aggregate(amount_paid=Sum("amount_paid"))
            billingdetails = obj.billingdetail_set.filter(billing_id=obj.id).aggregate(
                amount_paid=Sum("amount_paid")
            )
            sum_total = extrapayment["amount_paid"] + billingdetails["amount_paid"]

            return sum_total
        except Exception as e:
            print(e)

    def get_grand_outstanding(self, obj):
        try:
            billingdetails = obj.billingdetail_set.filter(billing_id=obj.id).aggregate(
                amount_paid=Sum("amount_paid")
            )
            extra_payment = obj.billingextrapayment_set.filter(
                billing_id=obj.id
            ).aggregate(amount_paid=Sum("amount_paid"))
            extra_item_fee = (
                obj.billingextrapayment_set.filter(billing_id=obj.id)
                .values("item_name_fee")
                .first()
            )
            total_amount_paid_details = 0
            total_amount_paid_extra = 0
            course_fee = (
                obj.billingdetail_set.filter(billing_id=obj.id)
                .values("course_fee")
                .first()
            )
            grand_total = extra_item_fee["item_name_fee"] + course_fee["course_fee"]
            if billingdetails and extra_payment:
                if (
                    total_amount_paid_details != None
                    and total_amount_paid_extra != None
                ):
                    total_amount_paid_details = billingdetails["amount_paid"]
                    total_amount_paid_extra = extra_payment["amount_paid"]

                    cal = grand_total - (
                        total_amount_paid_details + total_amount_paid_extra
                    )
                    return cal
                elif (
                    total_amount_paid_details == None
                    and total_amount_paid_extra == None
                ):
                    total_amount_paid_details = 0
                    total_amount_paid_extra = 0
                    cal = grand_total - (
                        total_amount_paid_details + total_amount_paid_extra
                    )

                    return cal
        except Exception as e:
            print(e)


class BillingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingDetail
        fields = ["id", "amount_paid", "date_paid"]


class PostBillingDetailSerializer(serializers.ModelSerializer):
    billing_id = serializers.IntegerField()

    class Meta:
        model = BillingDetail
        fields = ["id", "billing_id", "amount_paid", "program_type"]

    def validate_billing_id(self, value):
        if not Billing.objects.filter(id=value):
            raise serializers.ValidationError("Billing ID  is not found")
        return value

    def save(self, **kwargs):
        billing_id = self.validated_data["billing_id"]
        amount_paid = self.validated_data["amount_paid"]
        program_type = self.validated_data["program_type"]

        try:
            # create the billing details wrt billing_id
            billingdetails = BillingDetail.objects.create(
                billing_id=billing_id,
                amount_paid=amount_paid,
                program_type=program_type,
            )

            billingdetails.save()
            return billingdetails
        except ValueError as e:
            return e


# End Billing Region


# Blog Region


class BlogPostSerializer(serializers.ModelSerializer):
    blog_category = serializers.StringRelatedField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            "id",
            "author",
            "blog_category",
            "title",
            "slug",
            "content",
            "short_content",
            "image_1",
            "image_2",
            "image_3",
            "status",
            "seo_keywords",
            "date_created",
            "date_updated",
        ]
        lookup_field = "slug"

    def get_author(self, obj):
        return f"{obj.user}"


# End Blog Region


class PostEmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = [
            "id",
            "contact_person",
            "contact_person_mobile",
            "company_name",
            "company_url",
            "date_created",
            "date_updated",
        ]
        extra_kwargs = {"company_url": {"required": False, "allow_null": True}}


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "enter your password"},
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "password confirmation"},
        source="password",
    )
    mobile_numbers = serializers.CharField(write_only=True)
    employer = PostEmployerSerializer()

    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            "id",
            "user_type",
            "username",
            "password",
            "password2",
            "email",
            "mobile_numbers",
            "employer",
        ]

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email already exists")
        return value

    def validate_username(self, value):
        username = value.lower()
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("User with this username already exists")
        return value

    def validate_user_type(self, value):
        user_type = value.lower()
        if not user_type == "employer":
            raise serializers.ValidationError("Employer can only register")
        return value

    def validate_password(self, value):
        data = self.get_initial()
        password = data.get("password")
        password2 = value
        if password != password2:
            raise serializers.ValidationError("Passwords must match")
        return value

    def validate_password2(self, value):
        data = self.get_initial()
        password = data.get("password")
        password2 = value
        if password != password2:
            raise serializers.ValidationError("Passwords must match")
        return value

    def create(self, validated_data):
        employer_data = validated_data.pop("employer")
        contact_person = employer_data.pop("contact_person")
        contact_person_mobile = employer_data.pop("contact_person_mobile")
        company_name = employer_data.pop("company_name")
        company_url = employer_data.pop("company_url")
        user_type = validated_data["user_type"]
        email = validated_data["email"]
        username = validated_data["username"]
        mobile_numbers = validated_data["mobile_numbers"]
        password = validated_data["password"]
        user = User.objects.create(
            user_type=user_type,
            email=email,
            username=username,
            mobile_numbers=mobile_numbers,
        )
        if password:
            user.set_password(password)
            user.save()
        Employer.objects.create(
            user=user,
            contact_person=contact_person,
            contact_person_mobile=contact_person_mobile,
            company_name=company_name,
            company_url=company_url,
        )
        return user

    def save(self, **kwargs):
        try:
            employer = self.validated_data.pop("employer")
            contact_person = employer.pop("contact_person")
            contact_person_mobile = employer.pop("contact_person_mobile")
            company_name = employer.pop("company_name")
            company_url = employer.pop("company_url")
            user_type = self.validated_data["user_type"]
            email = self.validated_data["email"]
            username = self.validated_data["username"]
            mobile_numbers = self.validated_data["mobile_numbers"]
            user = User.objects.create(
                user_type=user_type,
                email=email,
                username=username,
                mobile_numbers=mobile_numbers,
            )
            employerobj = Employer.objects.create(
                user=user,
                contact_person=contact_person,
                contact_person_mobile=contact_person_mobile,
                company_name=company_name,
                company_url=company_url,
            )

            
            send_employer_sign_up_email(email)
            
            return user
        except Exception as e:
            print(e)        