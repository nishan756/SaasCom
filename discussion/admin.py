from django.contrib import admin
from .models import Discussion


@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ["author" , "title" , "posted_at"]
    search_fields = ["author__username"]