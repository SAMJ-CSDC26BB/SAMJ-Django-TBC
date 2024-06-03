from django.contrib import admin
from .models import GlobalSettings, CallForwardingRecords, User, TbcDestination

# Register your models here.
admin.site.register(GlobalSettings)
admin.site.register(CallForwardingRecords)
admin.site.register(User)


admin.site.register(TbcDestination)
