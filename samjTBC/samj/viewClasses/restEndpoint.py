from django.http import HttpResponse, JsonResponse
from django.views import View
from ..businessLogic import getDestination
import logging

class restEndpoint(View):
    def get(self, request):
        logger = logging.getLogger("samj")
        query = request.GET.get('number', '')
        logger.info("query -> " + query)
        dest = getDestination(query)
        logger.info("dest -> " + dest)
        return HttpResponse(dest)


        
