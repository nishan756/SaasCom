from .views import dashboard_entry_point , apps_dashboard , app_stats , my_applications , discussion_dashboard , jobs_dashboard , job_stats , job_applications , update_application_status , application_detail
from django.urls import path

urlpatterns = [
    path('entry-point/' , dashboard_entry_point , name = "dashboard-entry-point"),
    # Apps related urls
    path('apps/' , apps_dashboard , name = "apps-dashboard"),
    path('apps/stats/<uuid:id>/' , app_stats , name = "app-stats"),

    # Jobs related URLS
    path("my-applications/" , my_applications , name = "my-applications"),
    path("jobs/" , jobs_dashboard , name = "jobs-dashboard"),
    path("jobs/applications/<uuid:id>" , job_applications , name = "job-applications"),
    path("job/update-application-status/<uuid:id>/<str:status>/" , update_application_status , name = "update-application-status"),
    path("application-detail/<str:id>/" , application_detail , name = "application-detail"),
    path("job/stats/<uuid:id>/" , job_stats , name = "job-stats"),

    # Dsicussion related URLS
    path("discussion/" , discussion_dashboard , name = "discussion-dashboard"),

]
