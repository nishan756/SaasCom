from django.contrib import admin
from .models import Discussion , Tag


@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ["user" , "title" , "posted_at"]
    search_fields = ["user__username"]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["title"]