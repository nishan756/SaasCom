from .views import home , all_apps , app_detail , vote
from django.urls import path

urlpatterns = [
    path("all/" , all_apps , name = "all-apps"),
    path("<str:id>/" , app_detail , name = "app-detail"),
    path("<str:id>/vote/" , vote , name = "vote"),
]
