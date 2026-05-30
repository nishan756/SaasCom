from django.urls import path
from .views import create_discussion , delete_discussion , all_discussions , discussion_detail

urlpatterns = [
    path("" , all_discussions , name = "all-discussions"),
    path("<str:id>/" , discussion_detail , name = "discussion-detail"),
    path("create/" , create_discussion , name = "create-discussion"),
    path("delete/<str:id>/" , delete_discussion , name = "delete-discussion"),
]
