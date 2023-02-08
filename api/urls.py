from django.urls import path, include
from rest_framework_nested import routers
from . import views
from . import pdf

router = routers.DefaultRouter()
router.register('topbars', views.TopBarViewSet)
router.register('mainbanners', views.MainBannerViewSet)
router.register('sectionbanners', views.SectionBannerViewSet)
router.register('testimonials', views.TestimonialViewSet)
router.register('techicons', views.TechIconViewSet)
router.register('featuredprojects', views.FeaturedProjectViewSet)
router.register('componentdumps', views.ComponentDumpViewSet)
router.register('coursecategories', views.CourseCategoryViewSet)
router.register('courses', views.CourseViewSet, basename='courses')
router.register('teachers', views.TeacherViewSet)
router.register('students', views.StudentViewSet, basename='students')
router.register('navlinks', views.NavLinkViewSet)
router.register('shortquizes', views.ShortQuizViewSet)
router.register('inquiries', views.InquiryViewSet)

# new viewset implemented
router.register('enrollments',views.EnrollmentViewSet)
router.register('assignments',views.AssignmentViewSet, basename='assignment')
router.register('resources',views.ResourceViewSet, basename='resource')
router.register('projects',views.ProjectViewSet, basename='project')
router.register('coursemanuals',views.CourseManualViewSet, basename='coursemanual')
router.register('coursescards',views.CourseCardViewSet,basename='coursescard')
router.register('interestedforms',views.InterestedFormViewSet,basename='interestedform')
router.register('studentattendances',views.StudentAttendanceViewSet,basename='studentattendance')
router.register('coursehomepagefeatures', views.CourseHomepageFeatured,basename='homepagefeatured')
router.register('virtualclasses', views.VirtualClassViewSet, basename='virtualclasses')
router.register('kidscoding', views.KidsCodingViewSet,basename='kidscoding')
router.register('kidscodingcourses', views.KidsCodingCourseViewSet, basename='kidscodingcourses')
router.register('coursedetails',views.CourseDetailsViewSet, basename='coursedetails')
router.register('courseoutlines', views.CourseOutlineViewSet,basename='courseoutlines')
router.register('coursedetailsfeatured', views.CourseDetailsFeaturedViewSet, basename='coursedetailsfeatured')
router.register('kidscoursedetailsfeatured',views.KidCourseDetailsFeaturedViewSet, basename='kidscoursedetailsfeatured')

# Nested routes
courses_router = routers.NestedDefaultRouter(
    router, 'courses', lookup='course')
courses_router.register('schedules', views.ScheduleViewSet,
                        basename='course-schedules')

navlink_router = routers.NestedDefaultRouter(
    router, 'navlinks', lookup='navlink')
navlink_router.register(
    'items', views.NavLinkItemViewSet, basename='navlink-items')

coursemanual_router = routers.NestedDefaultRouter(router,'coursemanuals', lookup='coursemanuals')
coursemanual_router.register('coursesview',views.CoursesViewSet, basename='course')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(courses_router.urls)),
    path('', include(navlink_router.urls)),
    path('', include(coursemanual_router.urls)),
    path('auth/',include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/users/login',views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
