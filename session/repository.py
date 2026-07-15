from .models import User , Follow
from saas_com.core.exceptions import ObjectNotFound , AlreadyExists
from django.contrib.auth import authenticate
from django.db.models import Q , Count , Prefetch , Value
from django.db.models.functions import Concat
from apps.models import App

class UserRepo:

    def total_user(self):
        return User.objects.filter(is_active = True).count()

    def get_user(self , username):
        try:
            return User.objects.get(username = username)
        except User.DoesNotExist:
            raise ObjectNotFound("User not found")
    
    def check_user_with_email_or_username(self , email = None , username = None):
        
        if email:
            return User.objects.filter(email = email)
        
        return User.objects.filter(username = username)
    
    def get_users(self, user_type, **query_param):
        users = (
            User.objects
            .filter(user_type=user_type)
            .exclude(is_superuser=True, is_staff=True)
            .annotate(
                total_apps=Count("apps", distinct=True),
                total_follower=Count("followers", distinct=True),
                full_name = Concat("first_name" , Value(" ") , "last_name")
            )
        )

        if full_name := query_param.get("full_name"):
            users = users.filter(Q(full_name__icontains=full_name)|Q(full_name__icontains = full_name))
        return users.order_by(query_param.get("sort_by"))

    def view_profile(self , username):
        try:
            return User.objects.prefetch_related(Prefetch("apps" , App.objects.filter(status = "approved")) , "jobs" , "discussions").get(username = username)
        except User.DoesNotExist:
            raise ObjectNotFound("User not found")
    
    def signup(self , user):
        return user.save()

    def edit_profile(self , user_form):
        return user_form.save()

    def change_email(self , user , email):
        user.email = email
        return user.save()
    
    def authenticated(self , request , username , password):
        user = authenticate(request , username = username , password = password)
        if user is not None:
            return user
        raise ObjectNotFound("Invalid username or password")
        


class FollowRepo:

    def is_following(self , follower , following):
        return Follow.objects.filter(follower = follower , following = following).exists()
    
    def total_follower(self , user):
        return Follow.objects.filter(following = user).count()
    
    def total_following(self , user):
        return Follow.objects.filter(follower = user).count()

    def follow(self , follower , following):
        new_follow = Follow(follower = follower , following = following)
        new_follow.save()
    
    def unfollow(self , follower , following):
        follow = Follow.objects.get(follower = follower , following = following)
        follow.delete()
