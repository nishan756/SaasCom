from django.urls import path
from .views import vote

urlpatterns = [
    path("<str:content_type_str>/<str:id>/" , vote , name = "vote"),
]
