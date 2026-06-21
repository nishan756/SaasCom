from .views import dashboard_entry_point , apps_dashboard , app_stats , my_applications , discussion_dashboard , jobs_dashboard , job_stats
from django.urls import path

urlpatterns = [
    path('entry-point/' , dashboard_entry_point , name = "dashboard-entry-point"),
    # Apps related urls
    path('apps/' , apps_dashboard , name = "apps-dashboard"),
    path('apps/stats/<uuid:id>/' , app_stats , name = "app-stats"),

    # Jobs related URLS
    path("my-applications/" , my_applications , name = "my-applications"),
    path("jobs/" , jobs_dashboard , name = "jobs-dashboard"),
    path("job/stats/<uuid:id>/" , job_stats , name = "job-stats"),

    # Dsicussion related URLS
    path("discussion/" , discussion_dashboard , name = "discussion-dashboard"),

]
