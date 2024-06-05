from django.http import HttpResponse, JsonResponse
from django.views import View
from samj.models import CallForwardingRecords

class restEndpoint(View):
    def get(self, request):
        call_forwarding_records = CallForwardingRecords.objects.all()
        names = [record.Name for record in call_forwarding_records]
        print(call_forwarding_records)
        return HttpResponse(names)
