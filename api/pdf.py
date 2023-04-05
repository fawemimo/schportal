import os

from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import HttpResponse
# PDF CONFIG
from django.template.loader import get_template
from xhtml2pdf import pisa

from api.models import *


def link_callback(uri, rel):

    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        sUrl = settings.STATIC_URL
        sRoot = settings.STATIC_ROOT
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri
    if not os.path.isfile(path):
        raise Exception("media URI must start with %s or %s" % (sUrl, mUrl))
    return path


def create_receipts(self, billing_pk, pk):
    billings = Billing.objects.get(id=billing_pk)
    billingdetails = BillingDetail.objects.get(billing_id=billings.id, id=pk)
    context = {"billingdetails": billingdetails}
    template_path = "api/billings_receipt.html"
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"filename='{billings.id}_billings_receipt.pdf'"
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")
    return response
