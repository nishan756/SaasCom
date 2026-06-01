from .views import post_comment , delete_comment
from django.urls import path

urlpatterns = [
    path("post/<str:content_type>/<uuid:id>/" , post_comment , name = "post-comment"),
    path("delete/<uuid:id>/" , delete_comment , name = "delete-comment"),
]

