from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("accounts.api_urls")),
    path("api/", include("posts.api_urls")),
    path("", include("posts.urls")),
    path("accounts/", include("accounts.urls")),
]
