from .repository import UserRepo , FollowRepo
from saas_com.core.exceptions import FollowException, InvalidForm , InvalidContentType
from django.contrib.auth import update_session_auth_hash
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


class UserService:
    repo = UserRepo()

    def total_user(self):
        return self.repo.total_user()

    def get_user(self , username):
        return self.repo.get_user(username)
    
    def view_profile(self , username):
        return self.repo.view_profile(username)
    
    def get_users(self , user_type):
        return self.repo.get_users(user_type = user_type)
    
    def signup(self , form):
        if form.is_valid():
            user = form.save()
            return self.repo.signup(user)
        raise InvalidForm((form.errors))

    def edit_profile(self , user_form):
        if user_form.is_valid():
            return self.repo.edit_profile(user_form)
        raise InvalidForm(user_form.errors)

    def change_password(self , request , form):
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request , user)
        raise InvalidForm(form.errors)
    
    def authenticated(self , form , request):
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            return self.repo.authenticated(request, username, password)
        raise InvalidForm("Invalid form data")
    

class FollowService:
    repo = FollowRepo()

    def is_following(self , follower , following):
        return self.repo.is_following(follower, following)
    
    def total_follower(self , user):
        return self.repo.total_follower(user = user)
    
    def total_following(self , user):
        return self.repo.total_following(user = user)

    def follow(self , follower , following):
        if follower == following:
            raise FollowException("You cannot follow yourself.")
        if not self.repo.is_following(follower, following):
            return self.repo.follow(follower, following)
        else:
            raise FollowException("You are already following this user.")
    
    def unfollow(self , follower , following):
        if follower == following:
            raise FollowException("You cannot unfollow yourself.")
        if self.repo.is_following(follower, following):
            return self.repo.unfollow(follower, following)
        else:
            raise FollowException("You are not following this user.")


class EmailService:

    @staticmethod
    def send_email(subject, recipient, template_name, context = None):
        context = context if context else {}

        html_content = render_to_string(
            template_name=template_name,
            context=context
        )

        email = EmailMultiAlternatives(
            subject=subject,
            body="",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient]
        )

        email.attach_alternative(
            html_content,
            "text/html"
        )

        email.send()

