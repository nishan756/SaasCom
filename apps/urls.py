from .views import create_app, home , all_apps , app_detail , vote , add_review , del_review , create_app , del_image
from django.urls import path

urlpatterns = [
    path("all/" , all_apps , name = "all-apps"),
    path("create-app/" , create_app , name = "create-app"),

    # Image related url
    path("del-image/<str:id>" , del_image , name = "del-image"),
    path("<str:id>/" , app_detail , name = "app-detail"),
    path("<str:id>/vote/" , vote , name = "vote"),
    path("<str:id>/review/add" , add_review , name = "add-review"),
    path("<str:id>/review/delete" , del_review , name = "del-review"),
]
