from django.shortcuts import render , redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from session.views import is_safe_url
from .service import ReportService
from saas_com.core.exceptions import InvalidForm , AlreadyExists , PermissionDenied , ObjectNotFound

# ===================SERVICES==============
report_service = ReportService()
# ===================FORMS=================
from .forms import ReportForm

@require_POST
@login_required(login_url = "login")
def report(request , content_type_str , id):
    HTTP_REFERER = is_safe_url(request.META.get("HTTP_REFERER") , allowed_hosts=request.get_host())
    try:
        report_service.add_report(reporter=request.user, content_type_str = content_type_str, id=id, form=ReportForm(request.POST))
        messages.success(request, "Your report has been submitted successfully.")
    
    except InvalidForm as e:
        messages.error(request, str(e))
    
    except AlreadyExists as e:
        messages.info(request , str(e))
    
    except PermissionDenied as e:
        messages.warning(request , str(e))
    
    except ObjectNotFound as e:
        messages.error(request , str(e))
    
    except Exception as e:
        messages.error(request, "An error occurred while submitting your report. Please try again later.")
    return redirect(HTTP_REFERER)

@require_POST
@login_required(login_url = "login")
def del_report(request , id):
    HTTP_REFERER = is_safe_url(request.META.get("HTTP_REFERER" , "/") , request.get_host())
    try:
        report_service.del_report(id = id , user = request.user)
        messages.success(request , "Successfully deleted your report")
    except ObjectNotFound as e:
        messages.error(request , str(e))
    except PermissionDenied as e:
        messages.warning(request , "You can\'t delete this report")
    except Exception as e:
        messages.error(request , 'Something went wrong')
    return redirect(HTTP_REFERER)
