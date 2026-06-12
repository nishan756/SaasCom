from django.shortcuts import render , redirect
from django.views.decorators.http import require_GET , require_POST
from django.contrib.auth.decorators import login_required
from .service import NotificationService
from saas_com.core.service import is_safe_url
from django.contrib import messages

notification_service = NotificationService()

@login_required(login_url = "login")
@require_GET
def notifications(request):
    is_read = request.GET.get("is_read")
    context = {}
    context["notifications"] = notification_service.get_notifications(request.user , is_read)
    return render(request , "notifications.html" , context)


@login_required(login_url = "login")
@require_POST
def mark_all_as_read(request):
    notification_service.mark_as_read(request.user)
    messages.success(request , "Marked notifications as read")
    return redirect('notifications')
