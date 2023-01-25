from api.models import Course
# PDF CONFIG
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.http import HttpResponse
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


def link_callback(uri, rel):

        result = finders.find(uri)
        if result:
                if not isinstance(result, (list, tuple)):
                        result = [result]
                result = list(os.path.realpath(path) for path in result)
                path=result[0]
        else:
                sUrl = settings.STATIC_URL        # Typically /static/
                sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                mUrl = settings.MEDIA_URL         # Typically /media/
                mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                if uri.startswith(mUrl):
                        path = os.path.join(mRoot, uri.replace(mUrl, ""))
                elif uri.startswith(sUrl):
                        path = os.path.join(sRoot, uri.replace(sUrl, ""))
                else:
                        return uri

        # make sure that file exists
        if not os.path.isfile(path):
                raise Exception(
                        'media URI must start with %s or %s' % (sUrl, mUrl)
                )
        return path


def create_pdf(self,slug):
    course = Course.objects.get(slug=slug)

    context = {
        'course': course
    }
    template_path = 'api/course_outline.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f"filename='{course.slug}_course_outline.pdf'"
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
    html, dest=response, link_callback=link_callback)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response