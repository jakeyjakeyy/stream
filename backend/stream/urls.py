from django.contrib import admin
from django.urls import path

from .views import *

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


def fake_view(*args, **kwargs):
    """This view should never be called because the URL paths
    that map here will be served by nginx directly.
    """
    raise Exception("This should never be called!")


urlpatterns = [
    path("start", start_stream),
    path("stop", stop_stream),
    path("live/<username>/index.m3u8", fake_view, name="hls-url"),
    path("info/<str:username>", UserStreamInfo.as_view(), name="stream-info"),
    path("token", TokenObtainPairView.as_view(), name="token"),
    path("token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
    path("account", Following.as_view(), name="account"),
    path("featured", Featured.as_view(), name="featured"),
]
