import csv

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models.aggregates import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path, reverse
from django.utils.html import format_html, urlencode

from api.forms import CsvImportAdminForm

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
    # def get_urls(self):
    #     urls = super().get_urls()
    #     new_urls = [path("uploads", self.uploads, name="uploads")]
    #     return new_urls + urls

    # def uploads(self, request):
    #     form = CsvImportAdminForm()
    #     data = {"form": form}
    #     return render(self.request, "admin/upload.html", data)

    list_display = ["id", "first_name", "last_name", "username", "email"]
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


@admin.register(TopBar)
class TopbarAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "bar_src"]


@admin.register(MainBanner)
class MainBannerAdmin(admin.ModelAdmin):
    list_display = ["title", "published", "banner_src"]
    list_display_links = ["title"]
    list_editable = ["published"]


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
    list_display = ["id", "is_published"]
    list_filter = ["is_published"]


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

    def course_categoryo(self, course):
        return course.coursecategory.title

    def get_queryset(self, request):
        return Course.objects.order_by("ordering")


# @admin.register(Enrollment)
# class EnrollmentAdmin(admin.ModelAdmin):
#     list_display = ["id", "course","full_name","mobile_number"]
#     list_select_related = ["course"]


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "course",
        "teacher",
        "startdate",
        "fee",
        "discounted_fee",
        "fee_dollar",
        "discounted_fee_dollar",
        "program_type",
    ]
    list_editable = ["startdate", "program_type"]
    list_select_related = ["course"]

    def course(self, schedule: Schedule):
        return schedule.course.title

    def teacher(self, teacher: Teacher):
        return f"{teacher.user}"


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


@admin.register(Enrollment)
class InterestsAdmin(admin.ModelAdmin):
    list_display = ["course_title", "full_name", "mobile", "email"]

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
    list_display = ["id", "full_name", "profile_pix", "student_idcard_id", "batch_name"]
    search_fields = ["user__first_name", "user__last_name__istartswith"]
    list_per_page = 25
    paginator = CachingPaginator
    list_select_related = ["user"]
    actions = ["export_to_csv"]

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


@admin.register(StudentBackup)
class BackupStudentAdmin(admin.ModelAdmin):
    list_display = ["id", "full_name", "profile_pix", "student_idcard_id"]
    search_fields = ["full_name"]
    list_per_page = 25
    paginator = CachingPaginator
    list_select_related = ["student"]
    actions = ["export_to_csv"]

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

    def profile_pix(self, instance):
        if instance.profile_pic.name != "":
            return format_html(
                f'<img src="{instance.profile_pic.url}" class="thumbnail"/>'
            )
        return "No Profile Pics Added"

    class Media:
        css = {"all": ["api/css/styles.css"]}


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ["name", "assignment_file", "date_posted"]
    search_fields = ["name"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "project_docs", "project_assigned", "date_posted"]


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ["title", "course", "total_students", "start_date", "end_date"]
    search_fields = ["title", "students__user__first_name__istartswith"]
    list_select_related = ["teacher", "course"]
    autocomplete_fields = ["students"]
    actions = ["export_to_csv"]

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
    autocomplete_fields = ["batch", "assignment"]
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
    list_display = ["title", "manual", "date_posted", "date_updated"]
    search_fields = ["title"]
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


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ["id", "contact_person", "location", "company_name", "date_created"]
    date_hierarchy = "date_created"
    search_fields = ["contact_person", "company_name"]
    ordering = [
        "company_name",
    ]
    list_per_page = 25


@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "date_created"]
    search_fields = ["title"]
    date_hierarchy = "date_created"
    ordering = ["title"]
    list_per_page = 25


@admin.register(JobExperience)
class JobExperienceAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    search_fields = ["title"]


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "employer",
        "job_title",
        "slug",
        "save_as",
        "close_job",
    ]
    list_editable = ["save_as", "close_job"]
    list_filter = ["date_posted", "date_updated"]
    ordering = ["-date_posted"]
    date_hierarchy = "date_posted"
    list_select_related = ["employer"]
    autocomplete_fields = ["job_category", "employer", "experience"]
    list_per_page = 25
    # preserve_filters = ['job_category']


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
@admin.register(BillingExtraPayment)
class BillingExtraPaymentAdmin(admin.ModelAdmin):

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
        "billing",
        "item_name",
        "item_name_fee",
        "amount_paid",
        "outstanding_amount",
        "date_created",
    ]
    list_editable = ["amount_paid"]
    list_per_page = 25
    actions = ["export_to_csv"]


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
        "student",
        "course_name",
        "course_fee",
        "grand_total_paid",
        "grand_outstanding",
        "payment_completion_status",
    ]
    list_filter = ["payment_completion_status"]
    readonly_fields = ["grand_total_paid", "grand_outstanding"]
    list_select_related = ["student"]
    list_editable = ["student"]
    autocomplete_fields = ["student"]
    search_fields = ["student"]
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
        "course_fee",
        "amount_paid",
        "outstanding_amount",
        "date_paid",
    ]
    list_filter = ["date_paid"]
    search_fields = ["billing"]
    list_select_related = ["billing"]
    autocomplete_fields = ["billing"]
    list_per_page = 25
    readonly_fields = ["outstanding_amount"]
    actions = ["export_to_csv"]
    list_editable = ["billing", "amount_paid"]


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
    prepopulated_fields = {"slug": ("title",)}


# END BLOG REGION
