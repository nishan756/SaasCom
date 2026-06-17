from django.contrib import admin
from .models import Job , JobCategory , Currency , Application , Skill
from django.contrib import messages



@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ["title" , "parent"]

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ["code"]

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ["user" , "category" , "posted_at" , "deadline" , "is_active"]
    list_filter = ['user' , "is_active" , "category"]
    actions = ["mark_as_inactive" , "mark_as_active"]
    list_per_page = 100

    @admin.action(description = "Mark selected jobs as inactive")
    def mark_as_inactive(self , request , queryset):
        try:
            obj_count = queryset.update(is_active = False)
            messages.success(request , f"{obj_count} job marked as inactive")
        except Exception as e:
            messages.error(request , f"An error occured while performing this operation: {str(e)}")
    
    @admin.action(description = "Mark selected jobs as active")
    def mark_as_active(self , request , queryset):
        try:
            obj_count = queryset.update(is_active = True)
            messages.success(request , f"{obj_count} job marked as active")
        except Exception as e:
            messages.error(request , f"An error occured while performing this operation:{str(e)}")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ["job" , "user" , "applied_at" , "status"]
    list_filter = ['job__user__username' , "job__category"]
    list_per_page = 100


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ["name"]