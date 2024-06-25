from django.shortcuts import render
from django.views.generic import TemplateView

class callingNumberManagement(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'callingNumberManagement.html')