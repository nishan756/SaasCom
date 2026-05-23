from .views import user_login , user_logout , follow , unfollow , view_profile , report , del_report , users , add_bookmark , del_bookmark
from django.urls import path


urlpatterns = [
    path("login" , user_login , name = "login"),
    path("logout" , user_logout , name = "logout"),
    path("follow/<str:id>/" , follow , name = "follow"),
    path("unfollow/<str:id>/" , unfollow , name = "unfollow"),
    path("users/<str:user_type>/" , users , name = "users"),
    path("profile/<str:username>/" , view_profile , name = "profile"),
    path("add-report/<str:content_type>/<str:id>/" , report , name = "add-report"),
    path("del-report/delete/<str:id>/" , del_report , name = "del-report"),
    path("add-bookmark/<str:content_type>/<str:object_id>" , add_bookmark , name = "add-bookmark"),
    path("del-bookmark/<str:id>" , del_bookmark , name = "delete-bookmark"),
]
