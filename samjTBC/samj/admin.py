from django.contrib import admin

from .models import GlobalSettings, User, CalledNumber, CallForwarding, DestinationNumber

# Register your models here.
admin.site.register(GlobalSettings)
admin.site.register(User)
admin.site.register(CallForwarding)
admin.site.register(CalledNumber)
admin.site.register(DestinationNumber)
