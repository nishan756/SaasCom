from .views import create_app, del_app ,  all_apps , app_detail , add_review , del_review , create_app , del_image , update_app
from django.urls import path

urlpatterns = [
    # App Related URLS
    path("all/" , all_apps , name = "all-apps"),
    path("create/" , create_app , name = "create-app"),
    path("update/<uuid:id>/" , update_app , name = "update-app"),
    path("delete/<uuid:id>" , del_app , name = "del-app"),

    # Image related url
    path("del-image/<str:id>" , del_image , name = "del-image"),
    path("<str:id>/" , app_detail , name = "app-detail"),
    path("review/add/<uuid:id>" , add_review , name = "add-review"),
    path("review/delete/<uuid:id>" , del_review , name = "del-review"),
]
