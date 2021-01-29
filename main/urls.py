from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from users import router as users_api_router

auth_api_url = []

if settings.DEBUG:
    auth_api_url.append(path("verify/", include("rest_framework.urls")))

api_url_patterns = [
    path("accounts/", include(users_api_router.router.urls)),
    path("auth/", include(auth_api_url)),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_url_patterns)),
]
