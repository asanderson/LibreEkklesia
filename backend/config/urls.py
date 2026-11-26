from django.conf import settings
from django.urls import path

from config.api import api

urlpatterns = [
    path("api/", api.urls),
]

if settings.ADMIN_ENABLED:
    from django.contrib import admin

    urlpatterns.append(path("admin/", admin.site.urls))
