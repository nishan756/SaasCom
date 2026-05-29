from .views import add_bookmark , del_bookmark

from django.urls import path

urlpatterns = [
    path("add-bookmark/<str:content_type>/<str:object_id>" , add_bookmark , name = "add-bookmark"),
    path("del-bookmark/<str:id>" , del_bookmark , name = "del-bookmark"),
]
