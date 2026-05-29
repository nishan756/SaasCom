from .views import user_login , user_logout , follow , unfollow , view_profile , users
from django.urls import path


urlpatterns = [
    path("login" , user_login , name = "login"),
    path("logout" , user_logout , name = "logout"),
    path("follow/<str:username>/" , follow , name = "follow"),
    path("unfollow/<str:username>/" , unfollow , name = "unfollow"),
    path("users/<str:user_type>/" , users , name = "users"),
    path("profile/<str:username>/" , view_profile , name = "profile"),
]
