from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.sitemaps.views import sitemap
from .sitemaps import *

sitemaps = {
    'coursecategory':CourseCategorySitemap,
    'course':CourseSitemap,
    'blog':BlogPostSitemap,
    'job':JobSitemap,
    'jobcategory': JobCategorySitemap,
    'jobexperience':JobExperienceSitemap,
    'jobtype':JobTypeSitemap,
    'jobloaction': JobLocationSitemap,
    'careerapplicant': CareerApplicantSitemap,
    'careeropening': CareerOpeningSitemap,
    'careercategory': CareerCategorySitemap
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
