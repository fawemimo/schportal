from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
from django import forms
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name','user_type'),
            },
        ),
    )


@admin.register(TopBar)
class TopbarAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'bar_src']


@admin.register(MainBanner)
class MainBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'published', 'banner_src']
    list_display_links = ['title']
    list_editable = ['published']


@admin.register(SectionBanner)
class SectionBannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'banner_src']


@admin.register(TechIcon)
class TechIconAdmin(admin.ModelAdmin):
    list_display = ['id', 'tech_name', 'published', 'icon_img', 'popup_src']
    list_editable = ['published']


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title','total_course']

    @admin.display(ordering='total_course')
    def total_course(self,obj):
        url = (
            reverse('admin:api_course_changelist')
            + '?'
            +urlencode({
                'coursecategory__id': str(obj.id)
            })
        )
        return format_html(f'<a href="{url}">{obj.total_course} Courses</a>')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            total_course=Count('course')
        )   


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = ['course_code', 'title',
                    'frontpage_featured', 'active', 'ordering', 'slug']
    list_editable = ['frontpage_featured', 'active', 'ordering']
    list_display_links = ['course_code', 'title']
    list_select_related = ['coursecategory']
    prepopulated_fields = {'slug': ('title',)}

    def course_category(self, course):
        return course.coursecategory.title


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):

    list_display = ['id', 'course', 'teacher',
                    'startdate', 'fee', 'discounted_fee']
    list_editable = ['startdate']
    list_select_related = ['course']

    def course(self, schedule: Schedule):
        return schedule.course.title

    def teacher(self, teacher: Teacher):
        return f'{teacher.user}'


@admin.register(NavLink)
class NavlinkAdmin(admin.ModelAdmin):

    list_display = ['id', 'title']


@admin.register(NavLinkItem)
class NavLinkItemAdmin(admin.ModelAdmin):

    list_display = ['id', 'item', 'item_url', 'navlink_header']

    def navlink_header(self, item: NavLinkItem):
        return item.navlink.title


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'fullname']
    search_fields = ['user__first_name__istartswith', 'user__last_name__istartswith']

    def fullname(self, teacher: Teacher):
        if teacher.user is None:
            return f'Teacher has no user object'
        return f'{teacher.user.first_name} {teacher.user.last_name}'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if request.user.is_superuser:
            return queryset
        return queryset.filter(id=request.user.id)    



@admin.register(ShortQuiz)
class ShortQuizAdmin(admin.ModelAdmin):

    list_display = ['id', 'fullname', 'mobile', 'email']


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):

    list_display = ['id', 'fullname', 'mobile', 'email']


@admin.register(InterestedForm)
class InterestsAdmin(admin.ModelAdmin):

    list_display = ['course_title', 'full_name', 'mobile', 'email']

    def course_title(self, obj):
        return obj.course.title


@admin.register(StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'batch', 'attendance_status', 'timestamp']
    list_select_related = ['student','batch']

    def student(self, obj):
        return f'{obj.student.user.first_name} {obj.student.user.last_name}'

    def batch(self, obj):
        return obj.batch.title

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if request.user.is_superuser:
            return queryset
        elif request.user.is_staff:
            return queryset.filter(batch__teacher__user=request.user.id)

    def save_model(self, request, obj, form, change):
        obj.batch.teacher.user = request.user
        return super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        formset.save()
        form.instance.save()

    def get_form(self, request, obj=None, **kwargs):
        request._obj_ = obj

        return super().get_form(request, **kwargs)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'student_idcard_id', 'batch_name']
    search_fields = ['user__first_name', 'user__last_name__istartswith']

    @admin.display(description='Student Name')
    def name(self, obj):
        return (f'{obj.user.first_name} {obj.user.last_name}').upper()

    def batch_name(self, obj):
        obj = obj.batch_set.values('title')
        for x in obj:
            return (x['title']).upper()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if request.user.is_superuser:
            return queryset
        return queryset.filter(batch__teacher__user=request.user)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'batch', 'training_date']

    def student(self, obj):
        return obj.student.user

    def course(self, obj):
        return obj.course.title

    def batch(self, obj):
        return obj.batch.title


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['batch', 'name', 'assignment_file','date_posted']
    search_fields = ['name','batch']
    autocomplete_fields = ['batch']
    list_select_related = ['batch']
    
    def batch(self, obj):
        return obj.batch.title

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if request.user.is_superuser:
            return queryset
        return queryset.filter(batch__teacher__user_id=request.user.id)

    def save_model(self, request, obj, form, change):
        obj.batch.teacher.user = request.user
        return super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        formset.save()
        form.instance.save()


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'project_docs', 'project_assigned', 'date_posted']


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ['title', 'total_students','start_date', 'end_date']
    search_fields = ['title']
    list_select_related = ['teacher']

    @admin.display(ordering='start_date')
    def total_students(self, obj):
        batch = Batch.objects.get(id=obj.id)
        student = Student.objects.prefetch_related('batch_set').filter(batch=batch).count()
        url = (
            reverse('admin:api_student_changelist')
            + '?'
            + urlencode({
                'batch__id': str(obj.id)
            })
        )

        return format_html(f'<a href="{url}">{student}</a>')
    

@admin.register(AssignmentAllocation)
class AssignmentAllocationAdmin(admin.ModelAdmin):
    list_display = ['student', 'assignment', 'supervisor', 'deadline']
    autocomplete_fields = ['student','assignment']   
    list_select_related = ['assignment','student','supervisor'] 

    def student(self, obj):
        return obj.student.user

    def assignment(self, obj):
        return obj.assignment.name

    def supervisor(self, obj):        
        return obj.supervisor.user

    def get_queryset(self,request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(supervisor__user=request.user)    

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'supervisor', None) is None:  
            obj.supervisor.user = request.user
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        form_class = super(AssignmentAllocationAdmin, self).get_form(request, obj, **kwargs)
        form_class(request.user)

        return form_class    

@admin.register(ProjectAllocation)
class ProjectAllocationAdmin(admin.ModelAdmin):
    list_display = ['student', 'project',
                    'supervisor', 'start_date', 'delivery_status']

    def student(self, obj):
        return obj.student.user

    def project(self, obj):
        return obj.project.name

    def supervisor(self, obj):
        return obj.supervisor.user


@admin.register(CourseManualAllocation)
class CourseManualAllocationAdmin(admin.ModelAdmin):
    list_display = ['student', 'course_manual', 'released_by', 'when_released']

    def student(self, obj):
        return obj.student.user

    def course_manual(self, obj):
        return obj.course_manual.title

    def release_by(self, obj):
        return obj.release_by.user


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['student_name',  'batch',  'published']
    list_editable = ['published']
    list_filter = ['batch']


@admin.register(KidsCoding)
class KidsCodingAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'mobile', 'age_bracket', 'remarks']


@admin.register(VirtualClass)
class VirtualClassAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'mobile', 'course']


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['resource_type', 'primer', 'cheat_sheat', 'published']
    list_filter = ['published']
    list_editable = ['published']

    def resource_type(self, obj):
        return obj.resource_type.name


@admin.register(ResourceType)
class ResourceTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'date_created']
    prepopulated_fields = {'slug': ('name',)}
