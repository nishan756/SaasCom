from .views import add_bookmark , del_bookmark , bookmarks

from django.urls import path

urlpatterns = [
    path("" , bookmarks , name = "bookmarks"),
    path("add-bookmark/<str:object_id>" , add_bookmark , name = "add-bookmark"),
    path("del-bookmark/<str:id>" , del_bookmark , name = "del-bookmark"),
]
