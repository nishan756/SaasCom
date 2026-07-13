from django.shortcuts import redirect, render
from django.contrib.auth import login , logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_GET , require_POST
from saas_com.core.exceptions import ObjectNotFound , InvalidForm , FollowException , AlreadyExists
from saas_com.core.service import is_safe_url
import time , random
from django.utils import timezone
import threading

# =================FORMS=================
from .forms import LoginForm , SignUpForm , EditProfileForm , CustomPasswordChangeForm , EmailChangeForm
from report.forms import ReportForm

# =================SERVICES=============
from .service import UserService , FollowService , EmailService
from report.service import ReportService
from jobs.service import JobService
from apps.service import ReviewService
user_service = UserService()
follow_service = FollowService()
review_service = ReviewService()
job_service = JobService()
report_service = ReportService()


def user_login(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = LoginForm(request.POST)
        try:
            user = user_service.authenticated(form, request)
            login(request , user)
            messages.success(request, "You have been logged in successfully.")

            # Redirection
            next_url = is_safe_url(request.POST.get("next" , None) , request.get_host())
            if next_url:

                return redirect(next_url)
            
            return redirect("home")

        except InvalidForm:
            messages.error(request, "Invalid form data.")

        except ObjectNotFound:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request , "login.html" , {"form":form})

@login_required(login_url = "login")
@require_GET
def user_logout(request):
    logout(request)
    messages.success(request , "You have been logged out successfully.")
    return redirect("home")

def user_signup(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        form = SignUpForm(data = request.POST , files = request.FILES)
        try:
            user_service.signup(form)
            messages.success(request , "Successfully created your account")
            return redirect("login")

        except InvalidForm as e:
            messages.warning(request , str(e))

        except Exception as e:
            messages.error(request , "Something went wrong")

    context = {
        'form' : SignUpForm()
    }

    return render(request , 'signup.html' , context)


@login_required(login_url = "login")
@require_POST
def follow(request , username):
    HTTP_REFERER = is_safe_url(request.META.get("HTTP_REFERER") , allowed_hosts=request.get_host())
    following_user = user_service.repo.get_user(username)
    follower = request.user
    try:
        follow_service.follow(follower, following_user)
        messages.success(request, f"You have started following {following_user.full_name()}.")
    except ObjectNotFound as e:
        messages.error(request, str(e))
    except FollowException as e:
        messages.error(request, str(e))
    return redirect(HTTP_REFERER)

@login_required(login_url = "login")
@require_POST
def unfollow(request , username):
    HTTP_REFERER = is_safe_url(request.META.get("HTTP_REFERER") , allowed_hosts=request.get_host())
    following_user = user_service.repo.get_user(username)
    follower = request.user
    try:
        follow_service.unfollow(follower, following_user)
        messages.success(request, f"You have unfollowed {following_user.full_name()}.")
    except ObjectNotFound as e:
        messages.error(request, str(e))
    except FollowException as e:
        messages.error(request, str(e))
    return redirect(HTTP_REFERER)


@require_GET
def view_profile(request , username):
    context = {}
    page = request.GET.get("page" , 1)
    try:
        context["profile"] = user_service.view_profile(username)

        context["total_follower"] = follow_service.total_follower(user = context["profile"])
        context["total_following"] = follow_service.total_following(user = context["profile"])
        context["report_form"] = ReportForm()

        if request.user.is_authenticated:
            context["is_following"] = follow_service.is_following(follower = request.user , following = context["profile"])
            context["user_report"] = report_service.has_user_report('user' , context["profile"].id , request.user)
        if context["profile"].is_company:
            context["jobs"] = job_service.get_user_jobs(context["profile"] , page)
    
    except ObjectNotFound as e:
        messages.error(request , str(e))
        return redirect("home")
    
    except Exception as e:
        messages.error(request , "Something went wrong")
        return redirect("home")
    
    return render(request , "profile.html" , context)

@require_GET
def users(request , user_type):
    context = {}
    context["user_type"] = user_type.capitalize()
    context["users"] = user_service.get_users(user_type = user_type)
    return render(request , "users.html" , context)

@login_required(login_url = "login")
def edit_profile(request):
    try:
        user = user_service.get_user(username = request.user.username)
    except ObjectNotFound as e:
        messages.error(request , str(e))
    except Exception as e:
        messages.info(request , "Something went wrong")
    
    if request.method == "POST":
        user_form = EditProfileForm(instance = user , data = request.POST , files = request.FILES)
        try:
            user_service.edit_profile(user_form)
            messages.success(request , "Successfully updated your profile")
            return redirect("profile" , user_form.instance.username)
        
        except InvalidForm as e:
            messages.info(request , str(e))
            
        except Exception as e:
            messages.error(request , "Something went wrong")
    context = {}
    context["user_form"] = EditProfileForm(instance = user)
    context["password_change_form"] = CustomPasswordChangeForm(user = request.user)
    context["email_change_form"] = EmailChangeForm()
    return render(request , "edit-profile.html" , context)

@login_required(login_url="login")
@require_POST
def change_email(request):
    form = EmailChangeForm(data=request.POST)

    if form.is_valid():
        try:
            email = form.cleaned_data["email"]

            if email == request.user.email:
                messages.info(request, "This is your existing email")
                return redirect("edit-profile")

            if user_service.check_user_with_email_or_username(email=email):
                messages.info(request, "User with this email already exists")
                return redirect("edit-profile")

            code = str(random.randint(100000, 999999))

            request.session["session_code"] = code
            request.session["email"] = email
            request.session[f"otp_attempts:{request.user.username}"] = 0
            request.session["code_expiry"] = timezone.now().timestamp() + 600 

            email_thread = threading.Thread(target = EmailService.send_email , args = ("Email change verification" , email, "send-code.html", {"code": code , "full_name": request.user.full_name}))
            email_thread.start()

            return render(request, "verification.html")

        except Exception as e:
            messages.error(request, "Something went wrong")
            return redirect("edit-profile")
    else:
        messages.error(request, str(form.errors))
        return redirect("edit-profile")


@login_required(login_url="login")
@require_POST
def verify_email(request):
    try:
        code = request.POST.get("code")
        session_code = request.session.get("session_code")
        email = request.session.get("email")
        expiry = request.session.get("code_expiry") 
        attempts = request.session.get(f"otp_attempts:{request.user.username}", 0)

        if attempts >= 3:
            messages.error(request, "Too many attempts. Request a new code.")
            return redirect("edit-profile")

        if not all([code, session_code, email, expiry]):
            messages.error(request, "Invalid request")
            return redirect("edit-profile")

        if time.time() > float(expiry):
            messages.error(request, "Code expired")
            return redirect("edit-profile")

        if code != session_code:
            request.session[f"otp_attempts:{request.user.username}"] = attempts + 1
            messages.error(request, "Invalid code")
            return render(request, "verification.html") 
        
        user_service.change_email(request.user, email)

        request.session.pop("session_code", None)
        request.session.pop("email", None)
        request.session.pop("code_expiry", None)
        request.session.pop(f"otp_attempts:{request.user.username}", None)

        messages.success(request, "Verification Successfull")
        return redirect("profile", username=request.user.username)

    except Exception as e:
        messages.error(request, "Something went wrong")
        return redirect("edit-profile")

@login_required(login_url = "login")
@require_POST
def change_password(request):
    HTTP_REFERER = is_safe_url(url = request.META.get("HTTP_REFERER") , allowed_hosts = request.get_host())
    form = CustomPasswordChangeForm(request.user , request.POST)
    try:
        is_updated = user_service.change_password(request , form)
        if is_updated:
            logout(request)
            messages.success(request , "Successfully changed your password. Please login again")
            return redirect("login")
    except InvalidForm as e:
        messages.info(request , str(e))
        
    except Exception as e:
           messages.error(request , "Something went wrong")
    
    return redirect(HTTP_REFERER)