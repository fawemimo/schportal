import csv

from django import forms
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models.aggregates import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path, reverse
from django.utils.html import format_html, urlencode
from django.utils.translation import ngettext

from api.forms import CsvImportAdminForm

from .emails import *
from .models import *

admin.site.site_header = "Anchorsoft Academy"
admin.site.site_title = "Anchorsoft Academy Admin"
admin.site.index_title = "Anchorsoft Academy Portal"


class CachingPaginator(Paginator):
    def _get_count(self):
        if not hasattr(self, "_count"):
            self._count = None

        if self._count is None:
            try:
                key = "adm:{0}:count".format(hash(self.object_list.query.__str__()))
                self._count = cache.get(key, -1)
                if self._count == -1:
                    self._count = super().count
                    cache.set(key, self._count, 3600)

            except:
                self._count = self.object_list.count()
        return self._count

    count = property(_get_count)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["id", "first_name", "last_name", "username", "email", "user_type"]
    list_display_links = ["id", "username", "email"]
    list_filter = ["user_type", "is_staff", "is_superuser", "is_active"]
    ordering = ["-id"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "user_type",
                ),
            },
        ),
    )


@admin.register(SEO)
class SEOAdmin(admin.ModelAdmin):
    list_display = ["id", "page_title", "page_name"]


@admin.register(LoanPartner)
class LoanPartnerAdmin(admin.ModelAdmin):
    list_display = ["id", "company_name", "contact_person", "mobile", "date_posted"]
    list_filter = ["date_posted"]


@admin.register(TopBar)
class TopbarAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "bar_src"]


@admin.register(MainBanner)
class MainBannerAdmin(admin.ModelAdmin):
    list_display = ["title", "published", "ordering"]
    list_display_links = ["title"]
    list_editable = ["published", "ordering"]
    list_filter = ["published"]


@admin.register(SectionBanner)
class SectionBannerAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "banner_src"]


@admin.register(TechIcon)
class TechIconAdmin(admin.ModelAdmin):
    list_display = ["id", "tech_name", "published", "icon_img", "popup_src"]
    list_editable = ["published"]


@admin.register(AboutUsSection)
class AboutUsSectionAdmin(admin.ModelAdmin):
    list_display = ["id", "about_intro", "ordering"]
    list_editable = ["ordering"]


@admin.register(StudentLoanSection)
class StudentLoanSectionAdmin(admin.ModelAdmin):
    list_display = ["id", "is_published"]
    list_editable = ["is_published"]


@admin.register(CareerSection)
class CareerSectionAdmin(admin.ModelAdmin):
    list_display = ["id"]


@admin.register(CareerOpening)
class CareerOpeningAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "job_location",
        "employment_type",
        "career_category",
        "is_published",
    ]
    list_filter = ["is_published"]
    search_fields = ["title"]
    list_editable = ["is_published"]


@admin.register(CareerCategory)
class CareerCategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "date_created", "date_updated"]


@admin.register(CareerApplicant)
class CareerApplicantAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "email",
        "mobile",
        "career_opening",
        "resume",
    ]
    list_filter = ["highest_qualification", "degree"]
    autocomplete_fields = ["career_opening"]
    readonly_fields = ["resume"]
    paginator = CachingPaginator
    list_select_related = ["career_opening"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("career_opening")


@admin.register(AlbumSection)
class AlbumSectionAdmin(admin.ModelAdmin):
    list_display = ["id", "is_published"]
    list_filter = ["is_published"]


@admin.register(AlumiConnectSection)
class AlumiConnectSectionAdmin(admin.ModelAdmin):
    list_display = ["id", "is_published"]
    list_filter = ["is_published"]


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "total_course"]

    @admin.display(ordering="total_course")
    def total_course(self, obj):
        url = (
            reverse("admin:api_course_changelist")
            + "?"
            + urlencode({"coursecategory__id": str(obj.id)})
        )
        return format_html(f'<a href="{url}">{obj.total_course} Courses</a>')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(total_course=Count("course"))


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "course_code",
        "title",
        "is_virtual_class",
        "frontpage_featured",
        "published",
        "ordering",
        "slug",
    ]
    list_editable = ["frontpage_featured", "published", "is_virtual_class", "ordering"]
    list_display_links = ["course_code", "title"]
    list_select_related = ["coursecategory"]
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ["title"]
    paginator = CachingPaginator

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .order_by("ordering")
            .select_related("coursecategory")
        )


@admin.register(CorporateCourseSection)
class CorporateCourseSectionAdmin(admin.ModelAdmin):
    list_display = ["id"]


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "course",
        "active",
        "registration_status",
        "teacher",
        "startdate",
        "fee",
        "discounted_fee",
        "fee_dollar",
        "discounted_fee_dollar",
        "program_type",
    ]
    list_display_links = ["id", "course"]
    list_filter = ["active", "program_type", "registration_status"]
    list_editable = ["startdate", "program_type", "active", "registration_status"]
    list_select_related = ["course"]
    autocomplete_fields = ["course"]
    search_fields = [
        "course__title",
        "teacher__user__first_name",
        "teacher__user__first_name",
        "teacher__user__username",
    ]
    search_help_text = "Search for courses and teacher"

    def course(self, schedule: Schedule):
        return schedule.course.title

    def teacher(self, teacher: Teacher):
        return f"{teacher.user}"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("course")


@admin.register(CourseWaitingList)
class CourseWaitingListAdmin(admin.ModelAdmin):
    list_display = ["course", "first_name", "last_name", "email", "mobile"]


@admin.register(NavLink)
class NavlinkAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]


@admin.register(NavLinkItem)
class NavLinkItemAdmin(admin.ModelAdmin):
    list_display = ["id", "item", "item_url", "navlink_header"]

    def navlink_header(self, item: NavLinkItem):
        return item.navlink.title


@admin.register(ComponentDump)
class ComponentDumpAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ["id", "fullname", "courses"]
    search_fields = ["user__first_name__istartswith", "user__last_name__istartswith"]
    list_display_links = ["id", "fullname"]
    list_per_page = 25
    actions = ["export_to_csv"]
    autocomplete_fields = ["courses_taking"]

    @admin.display(description="Export as CSV")
    def export_to_csv(self, request, queryset):
        meta = self.model._meta
        fieldnames = [field.name for field in meta.fields]
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)

        writer = csv.writer(response)
        writer.writerow(fieldnames)
        for x in queryset:
            row = writer.writerow([getattr(x, field) for field in fieldnames])
        return response

    @admin.display(description="Total Courses Taking")
    def courses(self, obj):
        return obj.courses_taking.count()

    def fullname(self, teacher: Teacher):
        if teacher.user is None:
            return f"Teacher has no user object"
        return f"{teacher.user.first_name} {teacher.user.last_name}"

    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)

    #     if request.user.is_superuser:
    #         return queryset
    #     return queryset.filter(id=request.user.id)


@admin.register(ShortQuiz)
class ShortQuizAdmin(admin.ModelAdmin):
    list_display = ["id", "fullname", "mobile", "email"]


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ["id", "fullname", "mobile", "email"]
    paginator = CachingPaginator


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ["course_title", "full_name", "mobile", "email"]
    search_fields = ["full_name", "course__title"]
    search_help_text = "Full name and course title"
    list_select_related = ["course", "schedule"]
    list_filter = ["date_submitted"]
    date_hierarchy = "date_submitted"

    def course_title(self, obj):
        return obj.course.title


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = [
        "name_of_sponsor",
        "selection",
        "phone_number",
        "email",
        "number_of_student",
    ]
    search_fields = ["name_of_sponsor"]
    list_filter = ["selection"]
    ordering = ["name_of_sponsor"]


@admin.register(ScholarshipAward)
class ScholarshipAwardAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "sponsor",
        "award_date",
        "total_amount",
        "amount_received",
        "date_posted",
    ]
    list_per_page = 25
    autocomplete_fields = ["beneficiaries"]


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "announcement",
        "date_created",
        "expiration_date",
        "is_published",
    ]
    list_filter = ["is_published"]
    list_editable = ["expiration_date", "is_published"]


@admin.register(ScholarshipSection)
class ScholarshipSectionAdmin(admin.ModelAdmin):
    list_display = ["id", "scholarship_intro"]


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ["id", "main_title", "event_date", "date_posted", "ordering"]
    list_filter = ["event_date", "date_posted"]
    list_editable = ["event_date", "ordering"]
    search_fields = ["main_title"]


@admin.register(AlbumDetail)
class AlbumDetailAdmin(admin.ModelAdmin):
    list_display = ["id", "album", "title", "ordering", "date_created"]
    list_filter = ["date_created"]
    list_editable = ["ordering"]
    search_fields = ["title", "album__main_title"]


@admin.register(StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ["student_name", "batch_", "attendance", "timestamp"]
    list_select_related = ["student", "batch"]
    autocomplete_fields = ["student", "batch"]
    list_filter = ["batch", "timestamp", "attendance_status"]
    list_per_page = 25

    @admin.display(description="Batch Name")
    def batch_(self, obj):
        url = (
            reverse("admin:api_batch_changelist")
            + "?"
            + urlencode({"studentattendance__id": str(obj.id)})
        )
        return format_html(f'<a href="{url}">{obj.batch.title.upper()}</a>')

    def student_name(self, obj):
        return f"{obj.student.user.first_name} {obj.student.user.last_name}".upper()

    def attendance(self, obj):
        if obj.attendance_status == "Absent":
            return format_html('<img src="/static/admin/img/icon-no.svg" alt="False">')
        elif obj.attendance_status == "Present":
            return format_html('<img src="/static/admin/img/icon-yes.svg" alt="True">')
        else:
            return "No Attendance"

    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)

    #     if request.user.is_superuser:
    #         return queryset
    #     elif request.user.is_staff:
    #         return queryset.filter(batch__teacher__user=request.user.id)

    # def save_model(self, request, obj, form, change):
    #     obj.batch.teacher.user = request.user
    #     return super().save_model(request, obj, form, change)

    # def save_formset(self, request, form, formset, change):
    #     formset.save()
    #     form.instance.save()

    # def get_form(self, request, obj=None, **kwargs):
    #     request._obj_ = obj

    #     return super().get_form(request, **kwargs)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["id", "full_name", "profile_pix", "batch_name"]
    list_display_link = ["id", "full_name"]
    search_fields = ["user__first_name", "user__last_name__istartswith"]
    list_per_page = 25
    paginator = CachingPaginator
    list_select_related = ["user"]
    actions = ["export_to_csv"]
    fieldsets = (
        ("Privileges", {"fields": ("job_ready", "just_for_jobs")}),
        (
            "Student Information",
            {
                "fields": (
                    "user",
                    "full_name",
                    "date_of_birth",
                    "mobile_numbers",
                    "profile_pic",
                )
            },
        ),
        ("Job Credentials", {"fields": ("cv_upload",)}),
    )

    @admin.display(description="Export as CSV")
    def export_to_csv(self, request, queryset):
        meta = self.model._meta
        fieldnames = [field.name for field in meta.fields]
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)

        writer = csv.writer(response)
        writer.writerow(fieldnames)
        for x in queryset:
            row = writer.writerow([getattr(x, field) for field in fieldnames])
        return response

    def batch_name(self, obj):
        obj = obj.batch_set.values("title", "id")
        for x in obj:
            url = (
                reverse("admin:api_batch_changelist")
                + "?"
                + urlencode({"batch__id": str(x["id"])})
            )

            return format_html(f'<a href="{url}">{x["title"].upper()}</a>')

    def profile_pix(self, instance):
        if instance.profile_pic.name != "":
            return format_html(
                f'<img src="{instance.profile_pic.url}" class="thumbnail"/>'
            )
        return "No Profile Pics Added"

    class Media:
        css = {"all": ["api/css/styles.css"]}


@admin.register(Student_Matriculation)
class Student_MatriculationAdmin(admin.ModelAdmin):
    list_display = ["id", "student", "matric_number", "expel", "graduation_date"]
    list_editable = ["expel", "graduation_date"]
    autocomplete_fields = ["student"]
    list_filter = ["expel"]
    list_per_page = 25


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ["name", "assignment_file", "date_posted"]
    search_fields = ["name"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "project_docs", "project_assigned", "date_posted"]


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    actions = ["export_to_csv"]
    autocomplete_fields = ["students", "course"]
    list_display = [
        "id",
        "title",
        "course",
        "program_type",
        "total_students",
        "start_date",
        "end_date",
    ]
    list_filter = ["program_type", "start_date"]
    list_select_related = ["teacher", "course"]
    search_fields = ["title", "students__full_name", "course__title"]
    search_help_text = "Search for batch title, course title and students name"

    @admin.display(description="Export as CSV")
    def export_to_csv(self, request, queryset):
        meta = self.model._meta
        fieldnames = [field.name for field in meta.fields]
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)

        writer = csv.writer(response)
        writer.writerow(fieldnames)
        for x in queryset:
            row = writer.writerow([getattr(x, field) for field in fieldnames])
        return response

    @admin.display(ordering="start_date")
    def total_students(self, obj):
        batch = Batch.objects.get(id=obj.id)
        student = (
            Student.objects.prefetch_related("batch_set").filter(batch=batch).count()
        )
        url = (
            reverse("admin:api_student_changelist")
            + "?"
            + urlencode({"batch__id": str(obj.id)})
        )

        return format_html(f'<a href="{url}">{student}</a>')


@admin.register(AssignmentAllocation)
class AssignmentAllocationAdmin(admin.ModelAdmin):
    list_display = ["batch", "assignment", "supervisor", "deadline"]
    list_display_link = ["assignment"]
    autocomplete_fields = ["batch", "assignment", "supervisor"]
    list_select_related = ["assignment", "batch", "supervisor"]
    paginator = CachingPaginator

    def batch(self, obj):
        return obj.title

    def assignment(self, obj):
        return obj.assignment.name

    def supervisor(self, obj):
        return obj.supervisor.user


@admin.register(ProjectAllocation)
class ProjectAllocationAdmin(admin.ModelAdmin):
    list_display = ["student", "project", "supervisor", "start_date", "delivery_status"]

    def student(self, obj):
        return obj.student.user

    def project(self, obj):
        return obj.project.name

    def supervisor(self, obj):
        return obj.supervisor.user


@admin.register(CourseManual)
class CourseManualAdmin(admin.ModelAdmin):
    autocomplete_fields = ["course"]
    list_display = ["title", "manual", "date_posted", "date_updated"]
    search_fields = ["title", "course__title"]
    search_help_text = "Search for course manual title and course"
    list_filter = ["date_posted", "date_updated"]
    list_per_page = 25


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ["student_name", "batch", "published"]
    list_editable = ["published"]
    list_filter = ["batch"]


@admin.register(KidsCoding)
class KidsCodingAdmin(admin.ModelAdmin):
    list_display = ["full_name", "email", "mobile", "age_bracket", "remarks"]


@admin.register(VirtualClass)
class VirtualClassAdmin(admin.ModelAdmin):
    list_display = ["full_name", "email", "mobile", "course", "country_of_residence"]


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ["resource_type", "primer", "cheat_sheat", "published"]
    list_filter = ["published"]
    list_editable = ["published"]

    def resource_type(self, obj):
        return obj.resource_type.name


@admin.register(ResourceType)
class ResourceTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "date_created"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(InternationalModel)
class InternationalModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "country_name",
        "flag",
        "country_code",
        "topbar_src",
        "why_choose_virtual",
    ]


@admin.register(FeaturedProject)
class FeaturedProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "student_name", "course_taken", "batch", "published"]


@admin.register(FinancialAid)
class FinancialAidAdmin(admin.ModelAdmin):
    list_display = ["name", "course", "email", "mobile", "date_posted"]
    list_filter = ["date_posted"]

    def name(self, obj):
        return f"{obj.first_name} {obj.last_name}".upper()


@admin.register(CommunityConnect)
class CommunityConnectAdmin(admin.ModelAdmin):
    list_display = ["title", "completed", "community", "start_date", "ordering"]
    list_filter = ["start_date", "completed"]
    list_editable = ["ordering"]


@admin.register(AlumiConnect)
class AlumiConnectAdmin(admin.ModelAdmin):
    list_display = ["name", "title", "date_posted"]
    list_filter = ["date_posted"]

    def name(self, obj):
        return f"{obj.first_name} {obj.last_name}".upper()


@admin.register(TermsOfService)
class TermsOfServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "title")


@admin.register(VirtualVsOther)
class VirtualVsOthersAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "descriptions"]


@admin.register(HowItWork)
class VirtualHowItWorksAdmin(admin.ModelAdmin):
    list_display = ["id", "content"]


@admin.register(OurTeam)
class OurTeamAdmin(admin.ModelAdmin):
    list_display = ["id", "image", "full_name", "designation", "social_dump"]
    list_display_link = ["id", "full_name"]


# JobPortal region
class BaseJobSelectionAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "ordering", "date_created"]
    list_editable = ["ordering"]
    search_fields = ["title"]
    date_hierarchy = "date_created"
    ordering = ["title"]
    ordering = ["-ordering"]
    list_per_page = 25


@admin.register(JobType)
class JobTypeAdmin(BaseJobSelectionAdmin):
    pass


@admin.register(JobLocation)
class JobLocationAdmin(BaseJobSelectionAdmin):
    pass


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    @admin.action(description="Export as CSV")
    def export_to_csv(self, request, queryset):
        meta = self.model._meta
        fieldnames = [field.name for field in meta.fields]
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)

        writer = csv.writer(response)
        writer.writerow(fieldnames)
        for x in queryset:
            row = writer.writerow([getattr(x, field) for field in fieldnames])
        return response

    @admin.action(description="Make Approval")
    def make_approval(self, request, queryset):
        try:
            queryset.update(profile_approval=True)

            self.message_user(
                request,
                ngettext(
                    "%d Employer was successfully approved.",
                    "%d Employers were successfully approved.",
                    queryset,
                )
                % queryset,
                messages.SUCCESS,
            )

        except Exception as e:
            print(e)

    @admin.action(description="Make Disapproval")
    def disapprove(self, request, queryset):
        try:
            queryset.update(profile_approval=False)

            self.message_user(
                request,
                ngettext(
                    "%d Employer was successfully disapproved.",
                    "%d Employers were successfully disapproved.",
                    queryset,
                )
                % queryset,
                messages.SUCCESS,
            )

        except Exception as e:
            print(e)

    list_display = [
        "id",
        "contact_person",
        "location",
        "company_name",
        "profile_approval",
        "date_created",
        "date_updated",
    ]
    list_filter = ["profile_approval"]
    list_editable = ["profile_approval"]
    list_display_links = ["id", "contact_person", "company_name"]
    date_hierarchy = "date_created"
    search_fields = ["contact_person", "company_name"]
    ordering = [
        "-date_updated",
    ]
    actions = ["export_to_csv", "make_approval", "disapprove"]
    list_per_page = 25


@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "ordering", "date_created"]
    list_editable = ["ordering"]
    search_fields = ["title"]
    date_hierarchy = "date_created"
    ordering = ["title"]
    ordering = ["ordering"]
    list_per_page = 25


@admin.register(JobExperience)
class JobExperienceAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "ordering"]
    list_editable = ["ordering"]
    search_fields = ["title"]
    ordering = ["-ordering"]
    list_per_page = 25


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "employer",
        "job_type",
        "job_location",
        "job_title",
        "slug",
        "posting_approval",
        "close_job",
    ]
    list_editable = ["posting_approval", "close_job"]
    list_filter = ["date_posted", "date_updated"]
    ordering = ["-date_posted"]
    date_hierarchy = "date_posted"
    list_select_related = ["employer", "job_type", "job_location"]
    autocomplete_fields = [
        "job_category",
        "employer",
        "experience",
        "job_type",
        "job_location",
    ]
    list_per_page = 25

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("employer", "job_type", "job_location")
        )


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ["student", "job", "date_applied"]
    search_fields = ["student"]
    autocomplete_fields = ["student"]
    date_hierarchy = "date_applied"
    ordering = ["-date_applied"]
    list_select_related = ["student", "job"]


# end JobPortal region


# Billing region


@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    @admin.display(description="Export as CSV")
    def export_to_csv(self, request, queryset):
        meta = self.model._meta
        fieldnames = [field.name for field in meta.fields]
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)

        writer = csv.writer(response)
        writer.writerow(fieldnames)
        for x in queryset:
            row = writer.writerow([getattr(x, field) for field in fieldnames])
        return response

    list_display = [
        "id",
        "receipt_no",
        "student",
        "course_name",
        "program_type",
        "course_fee",
        "total_amount",
        "total_amount_text",
        "payment_completion_status",
    ]
    list_filter = ["payment_completion_status", "program_type"]
    list_select_related = ["student"]
    list_editable = ["student"]
    autocomplete_fields = ["student", "course_name", "sponsor"]
    search_fields = ["student__full_name", "course_name__title", "receipt_no"]
    search_help_text = "Student fullname, course name and receipt number"
    list_per_page = 25
    paginator = CachingPaginator
    actions = ["export_to_csv"]


@admin.register(BillingDetail)
class BillingDetailAdmin(admin.ModelAdmin):
    @admin.display(description="Export as CSV")
    def export_to_csv(self, request, queryset):
        meta = self.model._meta
        fieldnames = [field.name for field in meta.fields]
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)

        writer = csv.writer(response)
        writer.writerow(fieldnames)
        for x in queryset:
            row = writer.writerow([getattr(x, field) for field in fieldnames])
        return response

    def get_queryset(self, request):
        return BillingDetail.objects.select_related("billing")

    list_display = [
        "id",
        "billing",
        "amount_paid",
        "payment_descriptions",
        "date_paid",
    ]
    list_filter = ["date_paid"]
    search_fields = [
        "billing__student__full_name",
    ]
    search_help_text = "student full name"
    list_select_related = ["billing"]
    autocomplete_fields = ["billing"]
    list_per_page = 25
    actions = ["export_to_csv"]
    list_editable = ["billing", "amount_paid", "payment_descriptions"]


# End Billing


# BLOG REGION
@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "seo_keywords", "date_created", "date_updated"]
    list_filter = ["date_created", "date_updated"]
    search_fields = ["title"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "title",
        "status",
        "blog_category",
        "date_created",
        "date_updated",
    ]
    list_filter = ["date_created", "date_updated"]
    search_fields = ["title", "content"]
    list_editable = ["status"]
    list_select_related = ["blog_category"]
    autocomplete_fields = ["blog_category", "user"]
    prepopulated_fields = {"slug": ("title",)}


# END BLOG REGION


# FORUM ADMIN API


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ["title", "date_posted"]
    list_filter = ["date_posted"]
    search_fields = ["title"]
    search_help_text = "Search for topics"


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    autocomplete_fields = ["student", "topics"]
    list_display = ["id","student","batch", "title", "likes", "dislikes", "date_posted"]
    list_filter = ["date_posted"]
    search_fields = ["title"]

@admin.register(QuestionComment)
class QuestionCommentAdmin(admin.ModelAdmin):
    autocomplete_fields = ["student", "question"]
    list_display = [
        "student",
        "question",
        "is_correct",
        "likes",
        "dislikes",
        "date_commented",
    ]
    list_editable = ["is_correct"]
    list_filter = ["is_correct","date_commented"]


# END REGION FORUM ADMIN API
