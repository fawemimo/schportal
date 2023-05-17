from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from .sitemaps import *

sitemaps = {
    
    'about':AboutSitemap,
    'allCourses':AllCourseSitemap,
    'alljobs':AllJobsSitemap,
    'resourcesHomepage': AllResourceSitemap,
    'alumni': AlumiConnectSectionSitemap,
    'blog': AllBlogPostSitemap,
    'blog/slug':BlogPostSitemap,
    'careers': CareerSectionSitemap,
    'careeropening': CareerOpeningSitemap,
    'currentOpenings': AllCareerOpeningSitemap,
    'courses/location/area/slug':CourseDetailSitemap,
    'employer/postedjobs':EmployerPostedJobSitemap,
    'events':CommunityConnectSitemap,
    'international': InternationalModelSitemap,
    'kids-coding': KidsCodingCourseSitemap,
    'jobslug/:id':JobSitemap,
    'physical-class': PhysicalClassCourseSitemap,
    'resources/slug': ResourceSitemap,
    'scholarship':ScholarshipSectionSitemap,
    'students-loan': StudentLoanSectionSitemap,
    'terms':TermSitemap,
    'virtual-class':VirtualClassCourseSitemap,
}


urlpatterns = [
    path('contmgr/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', include('mainsite.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('sitemap.xml',sitemap,{'sitemaps':sitemaps},name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [ path('__debug__/', include('debug_toolbar.urls'))]
