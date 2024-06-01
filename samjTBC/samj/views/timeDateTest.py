from django.shortcuts import render
from django.views import View
import datetime

class TimeDateTest(View):
    def get(self, request):
        return render(request, "timeDateTest.html")
    