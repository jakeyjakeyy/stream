from django.contrib import admin
from django.urls import path

from .views import *


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
]
