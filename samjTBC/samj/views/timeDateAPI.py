from django.http import HttpResponse, JsonResponse
from django.views import View
import datetime

class TimeDateAPI(View):
    def get(self, request):
        return HttpResponse("+4367763106444")
#
#        now = datetime.datetime.now()
#        data = {
#            'time': now.strftime("%H:%M:%S"),
#            'day': now.strftime("%A"),
#            'date': now.strftime("%d.%m.%Y"),
#        }
#        return JsonResponse(data)
    