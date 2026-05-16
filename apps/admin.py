from django.contrib import admin
from .models import Category , App , AppImages , AppVote , Review , Tag
from django.utils.safestring import mark_safe
from django.contrib import messages

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_per_page = 50


class AppImagesInline(admin.TabularInline):
    model = AppImages
    extra = 1
    max_num = 5
    show_change_link = True

@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ["founder" , "name" , "view_logo" , "developed_at" , "status" , "added_at"]
    list_per_page = 50
    list_filter = ["status"]
    search_fields = ["name"]
    inlines = [AppImagesInline,]
    actions = ["mark_selected_apps_as_approved" , "mark_selected_apps_as_rejected"]

    def view_logo(self , obj):
        return mark_safe(f"<img src={obj.logo.url} width = '50px' height = '40px'>")
    
    @admin.action(description = "Mark selected apps as approved")
    def mark_selected_apps_as_approved(self , request , queryset):
        try:
            updated_count = queryset.update(status = "approved")
            messages.success(request , f"{updated_count} apps marked as approved")
        except Exception as e:
            messages.error(request , f"An error occurred: {str(e)}")
    
    @admin.action(description = "Mark selected apps as rejected")
    def mark_selected_apps_as_rejected(self , request , queryset):
        try:
            updated_count = queryset.update(status = "rejected")
            messages.success(request , f"{updated_count} apps marked as rejected")
        except Exception as e:
            messages.error(request , f"An error occurred: {str(e)}")

@admin.register(AppVote)
class AppVoteAdmin(admin.ModelAdmin):
    list_display = ["user" , "app" , "vote_type" , "added_at"]
    list_filter = ["vote_type"]
    list_per_page = 100


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["app" , "user" , "added_at"]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["title"]

