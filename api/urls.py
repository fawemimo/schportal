from django.urls import include, path
from rest_framework_nested import routers

from api import pdf

from . import views

router = routers.DefaultRouter()
router.register("topbars", views.TopBarViewSet)
router.register("mainbanners", views.MainBannerViewSet)
router.register("sectionbanners", views.SectionBannerViewSet)
router.register("testimonials", views.TestimonialViewSet)
router.register("aboutus", views.AboutUsSectionViewSet)
router.register(
    "studentloanbanners", views.StudentLoanSectionViewSet, basename="studentloanbanners"
)
router.register("techicons", views.TechIconViewSet)
router.register("featuredprojects", views.FeaturedProjectViewSet)
router.register("componentdumps", views.ComponentDumpViewSet)
router.register(
    "coursecategories", views.CourseCategoryViewSet, basename="coursecategories"
)
router.register("courses", views.CourseViewSet, basename="courses")
router.register("teachers", views.TeacherViewSet)
router.register("students", views.StudentViewSet, basename="students")
router.register("navlinks", views.NavLinkViewSet)
router.register("shortquizes", views.ShortQuizViewSet)
router.register("inquiries", views.InquiryViewSet)
router.register("profilepics", views.StudentUpdateViewSet, basename="profilepics")
router.register("careersections", views.CareerSectionViewSet)
router.register("albumsections", views.AlbumSectionViewSet)
router.register("alumiconnectsections", views.AlumiConnectSectionViewSet)


# new viewset implemented
router.register("assignments", views.AssignmentViewSet, basename="assignment")
router.register("resources", views.ResourceViewSet, basename="resource")
router.register("projects", views.ProjectViewSet, basename="project")
router.register("coursemanuals", views.CourseManualViewSet, basename="coursemanual")
router.register("coursescards", views.CourseCardViewSet, basename="coursescard")
router.register("interestedforms", views.EnrollmentViewSet, basename="interestedform")
router.register(
    "studentattendances", views.StudentAttendanceViewSet, basename="studentattendance"
)
router.register(
    "coursehomepagefeatures", views.CourseHomepageFeatured, basename="homepagefeatured"
)
# router.register("virtualclasses", views.VirtualClassViewSet, basename="virtualclasses")
router.register("kidscoding", views.KidsCodingViewSet, basename="kidscoding")
router.register(
    "kidscodingcourses", views.KidsCodingCourseViewSet, basename="kidscodingcourses"
)
router.register("coursedetails", views.CourseDetailsViewSet, basename="coursedetails")
router.register("courseoutlines", views.CourseOutlineViewSet, basename="courseoutlines")
router.register(
    "coursedetailsfeatured",
    views.CourseDetailsFeaturedViewSet,
    basename="coursedetailsfeatured",
)
router.register(
    "kidscoursedetailsfeatured",
    views.KidCourseDetailsFeaturedViewSet,
    basename="kidscoursedetailsfeatured",
)
router.register(
    "internationalmodels",
    views.InternationalModelViewSet,
    basename="internationalmodels",
)
router.register(
    "featuredvirtualclasses",
    views.FeaturedVirtualClassViewSet,
    basename="featuredvirtualclasses",
)
router.register("alumiconnects", views.AlumiConnectViewSet, basename="alumiconnects")
router.register(
    "communityconnects", views.CommunityConnectViewSet, basename="communityconnects"
)
router.register(
    "financialconnects", views.FinancialAidViewSet, basename="financialconnects"
)
router.register(
    "termsofservices", views.TermsOfServiceViewSet, basename="termsofservices"
)
router.register("howitworks", views.HowItWorksViewSet, basename="virtualhowitworks")
router.register(
    "virtualvsothers", views.VirtualVsOthersViewSet, basename="virtualvsothers"
)
router.register("ourteams", views.OurTeamViewSet, basename="ourteams")
router.register("sponsorships", views.SponsorshipsViewSet, basename="sponsorships")
router.register("announcements", views.AnnouncementViewSet, basename="announcements")
router.register(
    "scholarshipsections",
    views.ScholarshipSectionViewSet,
    basename="scholarshipsections",
)
router.register("albums", views.AlbumViewSet, basename="albums")

# JOB PORTAL REGION
router.register("employers", views.EmployerViewSet, basename="employerprofile")
router.register(
    "employerjobapplicants",
    views.EmployerJobApplicantViewSet,
    basename="employerjobapplicants",
)
router.register("jobs", views.JobViewSet, basename="jobs")
router.register(
    "studentappliedjobs", views.StudentAppliedJobViewSet, basename="studentappliedjobs"
)
router.register(
    "jobapplications", views.StudentApplicationForJobViewSet, basename="jobapplications"
)
router.register("applicants", views.ApplicantsViewSet, basename="applicants")
router.register("jobcategories", views.JobCategoryViewSet, basename="jobcategories")
router.register('jobexperiences', views.JobExperienceViewSet, basename="jobexperiences")
router.register('jobtypes', views.JobTypeViewSet, basename="jobtypes")
router.register('joblocations', views.JobLocationViewSet, basename="joblocations")

# END JOB PORTAL REGION


# Billing region

router.register("billings", views.BillingPaymentViewSet, basename="billings")
router.register(
    "billingdetails", views.BillingDetailsViewSet, basename="studentbillings"
)


# End Billing region


# BLOG POST REGION
router.register("blogposts", views.BlogPostViewSet, basename="blogposts")
# END BLOG POST REGION


# Nested routes
courses_router = routers.NestedDefaultRouter(router, "courses", lookup="course")
courses_router.register("schedules", views.ScheduleViewSet, basename="course-schedules")

navlink_router = routers.NestedDefaultRouter(router, "navlinks", lookup="navlink")
navlink_router.register("items", views.NavLinkItemViewSet, basename="navlink-items")

coursemanual_router = routers.NestedDefaultRouter(
    router, "coursemanuals", lookup="coursemanuals"
)
coursemanual_router.register("coursesview", views.CoursesViewSet, basename="course")

# billing_router = routers.NestedDefaultRouter(router, "billings", lookup="billing")
# billing_router.register(
#     "details", views.BillingDetailsViewSet, basename="billing-details"
# )


applicants_router = routers.NestedDefaultRouter(
    router, "employerjobapplicants", lookup="job"
)
applicants_router.register(
    "applicants", views.ApplicantsViewSet, basename="job-details"
)

urlpatterns = [
    path("", include(router.urls)),
    path("", include(courses_router.urls)),
    path("", include(navlink_router.urls)),
    path("", include(coursemanual_router.urls)),
    # path("", include(billing_router.urls)),
    path("", include(applicants_router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path(
        "auth/users/login",
        views.MyTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
]
