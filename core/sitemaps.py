from django.contrib.sitemaps import Sitemap

from api.choices import *
from api.models import *


class CourseSitemap(Sitemap):
        
    def items(self):       
        return Course.objects.order_by("ordering").select_related("coursecategory").filter(published=True)


class AllCourseSitemap(Sitemap):

    def items(self):
        return Course.objects.all()

    def location(self, item):
        return f'/courses/'


class CourseDetailSitemap(Sitemap):

    def items(self):
        return Course.objects.order_by("ordering").select_related("coursecategory").filter(published=True)

    def location(self, item):
        return f'/courses/{item.location_state}/{item.location_state_area}/{item.slug}/'


class PhysicalClassCourseSitemap(Sitemap):
    def items(self):
        course = Course.objects.order_by("ordering").select_related("coursecategory").filter(published=True)
        schedule = Schedule.objects.filter(course_id__in=course).filter(program_type='Onsite')
        return schedule

    def location(self, item):
        return f'/physical-class/'


class VirtualClassCourseSitemap(Sitemap):
    def items(self):
        course = Course.objects.order_by("ordering").select_related("coursecategory").filter(published=True)
        schedule = Schedule.objects.filter(course_id__in=course).filter(program_type='Virtual')
        return schedule

    def location(self, item):
        return f'/virtual-class/'

class KidsCodingCourseSitemap(Sitemap):

    def items(self):
        return  ( Course.objects.filter(kids_coding=True)
                .filter(published=True)
                .order_by("ordering")
                .select_related("coursecategory")
            )

    def location(self, item):
        return f'/kids-coding/'


class BlogPostSitemap(Sitemap):

    def items(self):
        return BlogPost.objects.all()

class AllBlogPostSitemap(Sitemap):

    def items(self):
        return BlogPost.objects.all()

    def location(self, item)    :
        return f'/blog/'

class AllJobsSitemap(Sitemap):

    def items(self):
        return (Job.objects.filter(posting_approval=True)
        .exclude(close_job=True)
        .select_related("employer", "job_type", "job_location")
        .prefetch_related("job_category", "experience")
    )

    def location(self, item):
        return (f'{JOB_BASE_URL}/')

        

class JobSitemap(Sitemap):

    def items(self):
        return (Job.objects.filter(posting_approval=True)
        .exclude(close_job=True)
        .select_related("employer", "job_type", "job_location")
        .prefetch_related("job_category", "experience")
    )


class CareerOpeningSitemap(Sitemap):

    def items(self):
        return CareerOpening.objects.all()

    def location(self, item):
        return f'/careers-openings/{item.id}'


class AllCareerOpeningSitemap(Sitemap):

    def items(self):
        return CareerOpening.objects.all()

    def location(self, item):
        return f'/careers-openings/'


class CareerSectionSitemap(Sitemap):

    def items(self):
        return CareerSection.objects.all()

    def location(self, item):
        return f'/careers/'

class EmployerPostedJobSitemap(Sitemap):

    def items(self):
        return (Job.objects
        .select_related("employer", "job_type", "job_location")
        .prefetch_related("job_category", "experience")
    )

    def location(self, item):
        return f'{JOB_BASE_URL}/employer/postedjobs/'


class AboutSitemap(Sitemap):

    def items(self):
        return AboutUsSection.objects.all()        


class InternationalModelSitemap(Sitemap):

    def items(self):
        return InternationalModel.objects.all()


class TermSitemap(Sitemap):

    def items(self):
        return TermsOfService.objects.all()


class CommunityConnectSitemap(Sitemap):

    def items(self):
        return CommunityConnect.objects.all()


class AlumiConnectSectionSitemap(Sitemap):

    def items(self):
        return AlumiConnectSection.objects.filter(is_published=True)


class ScholarshipSectionSitemap(Sitemap):        

    def items(self):
        return ScholarshipSection.objects.all()
    

class ResourceSitemap(Sitemap):

    def items(self):
        return Resource.objects.filter(published=True)



class AllResourceSitemap(Sitemap):

    def items(self):
        return Resource.objects.filter(published=True)

    def location(self, item):
        return f'/resources/'    


class StudentLoanSectionSitemap(Sitemap):

    def items(self):
        return StudentLoanSection.objects.filter(is_published=True)

    def location(self, item):
        return f'/students-loan/'