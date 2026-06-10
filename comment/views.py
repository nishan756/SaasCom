from django.shortcuts import render , redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.views import is_safe_url

# ===========FORMS==============
from .forms import CommentForm

# ===========SERVICES==============
from .service import CommentService

# ===========EXCEPTIONS============
from saas_com.core.exceptions import ObjectNotFound , InvalidForm

comment_service = CommentService()



@login_required(login_url="login")
@require_POST
def post_comment(request, content_type, id):

    HTTP_REFERER = request.META.get("HTTP_REFERER", "/")
    parent_id = request.POST.get("parent_id")
    content = request.POST.get("content")

    try:
        if parent_id:
            comment_service.reply_comment(
                user=request.user,
                parent_id=parent_id,
                content=content
            )
            messages.success(request, "Reply posted successfully")

        else:
            form = CommentForm(data=request.POST)

            comment_service.post_comment(
                user=request.user,
                content_type=content_type,
                object_id=id,
                form=form
            )
            messages.success(request, "Comment posted successfully")

    except ObjectNotFound as e:
        messages.error(request, str(e))

    except InvalidForm as e:
        messages.error(request, str(e))

    except Exception:
        messages.error(request, "Something went wrong")

    return redirect(HTTP_REFERER)


@login_required(login_url = "login")
@require_POST
def delete_comment(request , id):
    HTTP_REFERER = is_safe_url(request.META.get("HTTP_REFERER" , "/") , request.get_host())
    try:
        comment_service.delete_comment(user = request.user , id = id)
        messages.success(request , "Successfully deleted your comment")

    except ObjectNotFound as e:
        messages.error(request , str(e))
    
    except Exception as e:
        messages.error(request , "Something went wrong")
    
    return redirect(HTTP_REFERER)
