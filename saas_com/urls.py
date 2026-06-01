"""
URL configuration for saas_com project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from debug_toolbar.toolbar import debug_toolbar_urls

from apps.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home , name = "home"),
    path('apps/', include("apps.urls")),
    path('session/', include("session.urls")),
    path('jobs/', include("jobs.urls")),
    path('report/', include("report.urls")),
    path('vote/', include("vote.urls")),
    path('bookmark/', include("bookmark.urls")),
    path('discussion/', include("discussion.urls")),
    path('comment/', include("comment.urls")),
    path("summernote/" , include("django_summernote.urls"))
] + debug_toolbar_urls()
