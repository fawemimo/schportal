from django.contrib.sitemaps import Sitemap
from django.contrib.sites.shortcuts import get_current_site
from api.choices import *
from api.models import *
from . import settings


class CourseSitemap(Sitemap):
    def items(self):
        return (
            Course.objects.order_by("ordering")
            .select_related("coursecategory")
            .filter(published=True)
        )

    def get_domain(self, site=None):
        site = settings.DEFAULT_DOMAIN
        return site


class AllCourseSitemap(Sitemap):
    def items(self):
        return Course.objects.all()[:1]

    def location(self, item):
        return f"/courses/"

    def get_domain(self, site=None):
        site = settings.DEFAULT_DOMAIN
        return site


class CourseDetailSitemap(Sitemap):
    def items(self):
        return (
            Course.objects.order_by("ordering")
            .select_related("coursecategory")
            .filter(published=True)
        )

    def location(self, item):
        return f"/courses/{item.location_state}/{item.location_state_area}/{item.slug}/"

    def get_domain(self, site=None):
        site = settings.DEFAULT_DOMAIN
        return site


class PhysicalClassCourseSitemap(Sitemap):
    def items(self):
        course = (
            Course.objects.order_by("ordering")
            .select_related("coursecategory")
            .filter(published=True)
        )
        schedule = Schedule.objects.filter(course_id__in=course).filter(
            program_type="Onsite"
        )[:1]
        return schedule

    def location(self, item):
        return f"/physical-class/"

    def get_domain(self, site=None):
        site = settings.DEFAULT_DOMAIN
        return site


class VirtualClassCourseSitemap(Sitemap):
    def items(self):
        course = (
            Course.objects.order_by("ordering")
            .select_related("coursecategory")
            .filter(published=True)
        )
        schedule = Schedule.objects.filter(course_id__in=course).filter(
            program_type="Virtual"
        )[:1]
        return schedule

    def location(self, item):
        return f"/virtual-class/"

    def get_domain(self, site=None):
        site = settings.DEFAULT_DOMAIN
        return site


class KidsCodingCourseSitemap(Sitemap):
    def items(self):
        return (
            Course.objects.filter(kids_coding=True)
            .filter(published=True)
            .order_by("ordering")
            .select_related("coursecategory")
        )

    def location(self, item):
        return f"/kids-coding/"

    def get_domain(self, site=None):
        site = settings.DEFAULT_DOMAIN
        return site


class BlogPostSitemap(Sitemap):
    def items(self):
        return BlogPost.objects.all()

    def get_domain(self, site=None):
        site = settings.DEFAULT_DOMAIN
        return site


class AllBlogPostSitemap(Sitemap):
    def items(self):
        return BlogPost.objects.all()[:1]

    def location(self, item):
        return f"/blog/"

    def get_domain(self, site=None):
        site = settings.DEFAULT_DOMAIN
        return site


class AllJobsSitemap(Sitemap):
    def items(self):
        return (
            Job.objects.filter(posting_approval=True)
            .exclude(close_job=True)
            .select_related("employer", "job_type", "job_location")
            .prefetch_related("job_category", "experience")[:1]
        )

    def location(self, item):
        return f"{JOB_BASE_URL}/"

    def get_domain(self, site=None):
        site = settings.DEFAULT_DOMAIN
        return site


class JobSitemap(Sitemap):
    def items(self):
        return (
            Job.objects.filter(posting_approval=True)
            .exclude(close_job=True)
            .select_related("employer", "job_type", "job_location")
            .prefetch_related("job_category", "experience")
        )

    def get_domain(self, site=None):
        site = settings.DEFAULT_DOMAIN
        return site


class CareerOpeningSitemap(Sitemap):
    def items(self):
        return CareerOpening.objects.all()

    def location(self, item):
        return f"/careers-openings/{item.id}"

    def get_domain(self, site=None):
        site = settings.DEFAULT_DOMAIN
        return site


class AllCareerOpeningSitemap(Sitemap):
    def items(self):
        return CareerOpening.objects.all()[:1]

    def location(self, item):
        return f"/careers-openings/"

    def get_domain(self, site=None):
        site = settings.DEFAULT_DOMAIN
        return site


class CareerSectionSitemap(Sitemap):
    def items(self):
        return CareerSection.objects.all()

    def location(self, item):
        return f"/careers/"

    def get_domain(self, site=None):
        site = settings.DEFAULT_DOMAIN
        return site


class EmployerPostedJobSitemap(Sitemap):
    def items(self):
        return Job.objects.select_related(
            "employer", "job_type", "job_location"
        ).prefetch_related("job_category", "experience")[:1]

    def location(self, item):
        return f"{JOB_BASE_URL}/employer/postedjobs/"

    def get_domain(self, site=None):
        site = settings.DEFAULT_DOMAIN
        return site


class AboutSitemap(Sitemap):
    def items(self):
        return AboutUsSection.objects.all()

    def get_domain(self, site=None):
        site = settings.DEFAULT_DOMAIN
        return site


class InternationalModelSitemap(Sitemap):
    def items(self):
        return InternationalModel.objects.all()

    def get_domain(self, site=None):
        site = settings.DEFAULT_DOMAIN
        return site


class TermSitemap(Sitemap):
    def items(self):
        return TermsOfService.objects.all()

    def get_domain(self, site=None):
        site = settings.DEFAULT_DOMAIN
        return site


class CommunityConnectSitemap(Sitemap):
    def items(self):
        return CommunityConnect.objects.all()[:1]

    def get_domain(self, site=None):
        site = settings.DEFAULT_DOMAIN
        return site


class AlumiConnectSectionSitemap(Sitemap):
    def items(self):
        return AlumiConnectSection.objects.filter(is_published=True)

    def get_domain(self, site=None):
        site = settings.DEFAULT_DOMAIN
        return site


class ScholarshipSectionSitemap(Sitemap):
    def items(self):
        return ScholarshipSection.objects.all()

    def get_domain(self, site=None):
        site = settings.DEFAULT_DOMAIN
        return site


class ResourceSitemap(Sitemap):
    def items(self):
        return Resource.objects.filter(published=True)

    def get_domain(self, site=None):
        site = settings.DEFAULT_DOMAIN
        return site


class AllResourceSitemap(Sitemap):
    def items(self):
        return Resource.objects.filter(published=True)[:1]

    def location(self, item):
        return f"/resources/"

    def get_domain(self, site=None):
        site = settings.DEFAULT_DOMAIN
        return site


class StudentLoanSectionSitemap(Sitemap):
    def items(self):
        return StudentLoanSection.objects.filter(is_published=True)

    def location(self, item):
        return f"/students-loan/"

    def get_domain(self, site=None):
        site = settings.DEFAULT_DOMAIN
        return site
