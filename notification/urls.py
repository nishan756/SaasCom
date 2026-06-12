from .views import notifications , mark_all_as_read
from django.urls import path

urlpatterns = [
    path("" , notifications , name = "notifications"),
    path("mark_all_as_read/" , mark_all_as_read , name = "mark-all-as-read"),
]
