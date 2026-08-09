from .views import JobCategoryListCreateView , JobCategoryDetailUpdateDeleteView , SkillListCreateView , SkillDetailUpdateDeleteView , CurrencyListCreateView , CurrencyDetailUpdateDeleteView , JobListCreateView , JobDetailUpdateDeleteView
from django.urls import path

urlpatterns = [
    path("categories/" , JobCategoryListCreateView.as_view() , name = "categories"),
    path("categories/<int:id>/" , JobCategoryDetailUpdateDeleteView.as_view() , name = "category-detail"),

    path("skills/" , SkillListCreateView.as_view() , name = "skills"),
    path("skills/<int:id>/" , SkillDetailUpdateDeleteView.as_view() , name = "skill-detail"),

    path("currencies/" , CurrencyListCreateView.as_view() , name = "currencies"),
    path("currencies/<int:pk>/" , CurrencyDetailUpdateDeleteView.as_view() , name = "currency-detail"),

    path("all-jobs/" , JobListCreateView.as_view() , name = "all-jobs-api"),
    path("all-jobs/<str:id>/" , JobDetailUpdateDeleteView.as_view() , name = "job-detail-api"),

]
