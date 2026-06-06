from django.contrib import admin
from .models import Discussion


@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ["user" , "title" , "posted_at"]
    search_fields = ["user__username"]