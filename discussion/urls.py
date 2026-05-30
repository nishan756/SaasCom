from django.urls import path
from .views import post_discussion , delete_discussion , all_discussions , discussion_detail

urlpatterns = [
    path("" , all_discussions , name = "all-discussions"),
    path("<uuid:id>/" , discussion_detail , name = "discussion-detail"),
    path("post/" , post_discussion , name = "post-discussion"),
    path("<uuid:id>/delete/" , delete_discussion , name = "delete-discussion"),
]
