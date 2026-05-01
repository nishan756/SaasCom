from django.contrib import admin
from .models import Category , App , AppImages
from django.utils.safestring import mark_safe

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

    def view_logo(self , obj):
        return mark_safe(f"<img src={obj.logo.url} width = '50px' height = '40px'>")
