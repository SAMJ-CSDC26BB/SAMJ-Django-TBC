# samjTBC/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('samj.urls')),  # Ensure this line correctly includes the app's URLs
]
