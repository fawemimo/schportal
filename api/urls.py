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

# new viewset implemented
router.register('enrollment',views.EnrollmentViewSet)
router.register('assignment',views.AssignmentViewSet, basename='assignment')
router.register('resource',views.ResourceViewSet, basename='resource')
router.register('project',views.ProjectViewSet, basename='project')
router.register('coursemanual',views.CourseManualViewSet, basename='coursemanual')
router.register('coursesview', views.CoursesViewSet,basename='coursesview')
router.register('coursescard',views.CourseCardViewSet,basename='coursescard')
# Nested routes
courses_router = routers.NestedDefaultRouter(
    router, 'courses', lookup='course')
courses_router.register('schedules', views.ScheduleViewSet,
                        basename='course-schedules')

navlink_router = routers.NestedDefaultRouter(
    router, 'navlinks', lookup='navlink')
navlink_router.register(
    'items', views.NavLinkItemViewSet, basename='navlink-items')

coursemanual_router = routers.NestedDefaultRouter(router,'coursemanual', lookup='coursemanual')
coursemanual_router.register('coursesview',views.CoursesViewSet, basename='course')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(courses_router.urls)),
    path('', include(navlink_router.urls)),
    path('', include(coursemanual_router.urls))
]
