from django.contrib import admin
from .models import *


@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ("__str__", "started_at", "is_live")


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("__str__",)


@admin.register(Featured)
class FeaturedAdmin(admin.ModelAdmin):
    list_display = ("__str__",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
