from .views import post_job , all_jobs , job_detail , apply , applications , application_detail , update_application_status , my_applications , update_job

from django.urls import path

urlpatterns = [
    path("" , all_jobs , name = "all-jobs"),
    path("post-job/" , post_job , name = "post-job"),
    path("update-job/<uuid:id>/" , update_job , name = "update-job"),
    path("job-detail/<str:id>/" , job_detail , name = "job-detail"),

    # Application
    path("my-applications/" , my_applications , name = "my-applications"),
    path("apply/<str:id>/" , apply , name = "apply-job"),
    path("applications/<str:id>/" , applications , name = "applications"),
    path("application-detail/<str:id>/" , application_detail , name = "application-detail"),
    path("<str:status>/application/<str:id>/" , update_application_status , name = "update-application-status"),
    
]
