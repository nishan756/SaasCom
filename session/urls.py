from .views import user_signup , user_login , user_logout , follow , unfollow , view_profile , users , edit_profile , change_password
from django.urls import path


urlpatterns = [
    path("signup" , user_signup , name = "signup"),
    path("login" , user_login , name = "login"),
    path("logout" , user_logout , name = "logout"),
    path("follow/<str:username>/" , follow , name = "follow"),
    path("unfollow/<str:username>/" , unfollow , name = "unfollow"),
    path("users/<str:user_type>/" , users , name = "users"),
    path("profile/<str:username>/" , view_profile , name = "profile"),
    path("edit-profile/" , edit_profile , name = "edit-profile"),
    path("change-password/" , change_password , name = "change-password"),
]
