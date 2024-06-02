from django.contrib import admin
from .models import GlobalSettings, CallForwardingRecords, User

# Register your models here.
admin.site.register(GlobalSettings)
admin.site.register(CallForwardingRecords)
admin.site.register(User)
