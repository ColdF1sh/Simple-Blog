from django.urls import include, path

from .views import profile_edit_view, profile_view, register_view


urlpatterns = [
    path("register/", register_view, name="register"),
    path("profile/", profile_view, name="profile"),
    path("profile/edit/", profile_edit_view, name="profile_edit"),
    path("", include("django.contrib.auth.urls")),
]
