from django.http import HttpResponse, JsonResponse
from django.views import View
from samj.models import CallForwardingRecords
import logging

class restEndpoint(View):
    def get(self, request):
        #call_forwarding_records = CallForwardingRecords.objects.all()
        #names = [reco  rd.Name for record in call_forwarding_records]
        
        logger = logging.getLogger("samj")
        logger.info("This is a test log message")
        logger.error("This is a test log message")
        return HttpResponse("lol")
