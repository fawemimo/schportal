from django.contrib.sitemaps import Sitemap
from api.models import *


class CourseCategorySitemap(Sitemap):

    def items(self):
        return CourseCategory.objects.all()


class CourseSitemap(Sitemap):
        
    def items(self):       
        return Course.objects.all()


class BlogPostSitemap(Sitemap):

    def items(self):
        return BlogPost.objects.all()


class JobSitemap(Sitemap):

    def items(self):
        return Job.objects.all()


class JobCategorySitemap(Sitemap):

    def items(self):
        return JobCategory.objects.all()


class JobExperienceSitemap(Sitemap):

    def items(self):
        return JobExperience.objects.all()


class JobLocationSitemap(Sitemap):

    def items(self):
        return JobLocation.objects.all()


class JobTypeSitemap(Sitemap):

    def items(self):
        return JobType.objects.all()


class CareerCategorySitemap(Sitemap):

    def items(self):
        return CareerCategory.objects.all()
        

class CareerOpeningSitemap(Sitemap):

    def items(self):
        return CareerOpening.objects.all()


class CareerApplicantSitemap(Sitemap):

    def items(self):
        return CareerApplicant.objects.all()


