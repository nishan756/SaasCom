from django.contrib import admin

from .models import Notification

@admin.register(Notification)
class notificationAdmin(admin.ModelAdmin):
    list_display = ["recipient" , "event_type" , "created_at"]
