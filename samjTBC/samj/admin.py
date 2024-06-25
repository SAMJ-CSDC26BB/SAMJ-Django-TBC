from django.contrib import admin
from .models import GlobalSettings, User, CallForwarding, DestinationNumber, CalledNumber

# Register your models here.
admin.site.register(GlobalSettings)
admin.site.register(User)
admin.site.register(CallForwarding)
admin.site.register(DestinationNumber)
admin.site.register(CalledNumber)
