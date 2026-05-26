from .views import report , del_report
from django.urls import path

urlpatterns = [
    path("add-report/<str:content_type>/<str:id>/" , report , name = "add-report"),
    path("del-report/delete/<str:id>/" , del_report , name = "del-report"),
]
