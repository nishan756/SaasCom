from django.contrib import admin
from django.contrib.auth import get_user_model

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
                "fields":["first_name" , "last_name" , "username" , "email"  , "image" , "date_of_birth"],
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

    def full_name(self , obj):
        return f"{obj.first_name} {obj.last_name}"

    