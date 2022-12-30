from django.urls import path, include
from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register('topbars', views.TopBarViewSet)
router.register('mainbanners', views.MainBannerViewSet)
router.register('sectionbanners', views.SectionBannerViewSet)
router.register('testimonials', views.TestimonialViewSet)
router.register('techicons', views.TechIconViewSet)
router.register('featuredprojects', views.FeaturedProjectViewSet)
router.register('componentdumps', views.ComponentDumpViewSet)
router.register('coursecategories', views.CourseCategoryViewSet)
router.register('courses', views.CourseViewSet)
router.register('teachers', views.TeacherViewSet)
router.register('students', views.StudentViewSet)
router.register('navlinks', views.NavLinkViewSet)
router.register('shortquizes', views.ShortQuizViewSet)
router.register('inquiries', views.InquiryViewSet)


# Nested routes
courses_router = routers.NestedDefaultRouter(
    router, 'courses', lookup='course')
courses_router.register('schedules', views.ScheduleViewSet,
                        basename='course-schedules')

navlink_router = routers.NestedDefaultRouter(
    router, 'navlinks', lookup='navlink')
navlink_router.register(
    'items', views.NavLinkItemViewSet, basename='navlink-items')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(courses_router.urls)),
    path('', include(navlink_router.urls)),
]
