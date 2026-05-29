from django.contrib import admin
from .models import Vote

@admin.register(Vote)
class AppVoteAdmin(admin.ModelAdmin):
    list_display = ["user" ,"content_type" , "object_id" , "vote_type" , "added_at"]
    list_filter = ["content_type" , "vote_type"]
    list_per_page = 100
