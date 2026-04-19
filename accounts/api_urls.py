from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .api_views import ProfileAPIView


urlpatterns = [
    path("auth/token/", obtain_auth_token, name="api_auth_token"),
    path("profile/", ProfileAPIView.as_view(), name="api_profile"),
]
