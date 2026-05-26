from django.contrib import admin
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ["reporter" ,"report_type" ,"content_type" , "reported_at"]
    readonly_fields = ["reported_at"]
    list_per_page = 100
    search_fields = ["reporter__username" , "reason"]
