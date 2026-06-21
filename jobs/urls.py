from .views import post_job , all_jobs , job_detail , apply , update_job , delete_job

from django.urls import path

urlpatterns = [
    path("" , all_jobs , name = "all-jobs"),
    path("post-job/" , post_job , name = "post-job"),
    path("update-job/<uuid:id>/" , update_job , name = "update-job"),
    path("delete-job/<uuid:id>/" , delete_job , name = "delete-job"),
    path("job-detail/<str:id>/" , job_detail , name = "job-detail"),

    # Application
    path("apply/<str:id>/" , apply , name = "apply-job"),
    
]
