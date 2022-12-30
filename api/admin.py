from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2", "first_name", "last_name"),
            },
        ),
    )


@admin.register(TopBar)
class TopbarAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'bar_src']


@admin.register(MainBanner)
class MainBannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'banner_src']


@admin.register(SectionBanner)
class SectionBannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'banner_src']


@admin.register(TechIcon)
class TechIconAdmin(admin.ModelAdmin):
    list_display = ['id', 'tech_name', 'icon_img_src', 'popup_src']


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = ['id', 'title', 'description', 'course_category']
    list_editable = ['title']
    list_select_related = ['coursecategory']

    def course_category(self, course):
        return course.coursecategory.title


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):

    list_display = ['id', 'course', 'teacher',
                    'startdate', 'fee', 'discounted_fee']
    list_editable = ['startdate']

    def course(self, schedule: Schedule):
        return schedule.course.title

    def teacher(self, teacher: Teacher):
        return f'{teacher.first_name} {teacher.last_name}'


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

    list_display = ['id', 'first_name', 'last_name']


@admin.register(ShortQuiz)
class ShortQuizAdmin(admin.ModelAdmin):

    list_display = ['id', 'fullname', 'mobile', 'email']


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):

    list_display = ['id', 'fullname', 'mobile', 'email']
