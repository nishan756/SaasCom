from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Follow , Report

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["first_name" , "last_name" , "full_name" , "username" , "email"]
    list_per_page = 100
    search_fields = ["first_name" , "last_name" , "username"]
    readonly_fields = ["last_login" , "joined_at"]

    fieldsets = [

        (
            "Permissions and Groups",
            {
                "fields":["groups" , "user_permissions"]
            },
        ),

        (
            "Basic Info",
            {
                "fields":["first_name" , "last_name" , "username" , "email"  , "image" ,"gender" , "date_of_birth"],
            },
            
        ),

        (
            "Bio",
            {
                "fields":["bio"],
            },
            
        ),
        
        (
            "User Type",
            {
                "fields":["is_superuser" , "is_staff"],
            },
        ),

        (
            "Active Status",
            {
                "fields":["is_active"],
            },
        ),

        (
            "Joining Date and Last Login",
            {
                "fields":["last_login" , "joined_at"]
            },
        )
    ]


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ["follower" , "following"]
    list_per_page = 100
    search_fields = ["follower__username" , "following__username"]


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ["reporter" , "reason" , "reported_at"]
    readonly_fields = ["object_id" , "reported_at"]
    list_per_page = 100
    search_fields = ["reporter__username" , "reported_profile__username" , "reason"]