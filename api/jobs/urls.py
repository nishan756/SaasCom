from .views import JobCategoryView
from django.urls import path

urlpatterns = [
    path("categories/" , JobCategoryView.as_view() , name = "categories"),
    path("categories/<int:id>" , JobCategoryView.as_view() , name = "modify-category"),

]
