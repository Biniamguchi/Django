
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^', include('apps.surveys.urls')),
    url(r'^time_display/', include('apps.time_display.urls')),
    url(r'^admin/', admin.site.urls),
]
