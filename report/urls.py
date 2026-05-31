from .views import report , del_report
from django.urls import path

urlpatterns = [
    path("add-report/<str:id>/" , report , name = "add-report"),
    path("del-report/<str:id>/" , del_report , name = "del-report"),
]
