from .views import report , del_report
from django.urls import path

urlpatterns = [
    path("add/<str:content_type_str>/<str:id>/" , report , name = "add-report"),
    path("delete/<str:id>/" , del_report , name = "del-report"),
]
