from .views import user_login , user_logout , follow , unfollow , view_profile , report , del_report , users
from django.urls import path


urlpatterns = [
    path("login" , user_login , name = "login"),
    path("logout" , user_logout , name = "logout"),
    path("follow/<str:id>/" , follow , name = "follow"),
    path("unfollow/<str:id>/" , unfollow , name = "unfollow"),
    path("users/<str:user_type>/" , users , name = "users"),
    path("profile/<str:username>/" , view_profile , name = "profile"),
    path("report/<str:content_type>/<str:id>/" , report , name = "report"),
    path("report/delete/<str:id>/" , del_report , name = "del-report"),
]
