from .models import User , Follow
from saas_com.core.exceptions import ObjectNotFound
from django.contrib.auth import authenticate
from django.db.models import Q , Count , Prefetch
from apps.models import App

class UserRepo:

    def total_user(self):
        return User.objects.filter(is_active = True).count()

    def get_user(self , username):
        try:
            return User.objects.get(username = username)
        except User.DoesNotExist:
            raise ObjectNotFound("User not found")
    
    def get_users(self , user_type):
        users = User.objects.prefetch_related("apps" , "followers" , "following").filter(user_type = user_type).exclude(Q(is_superuser = True)|Q(is_staff = True)).annotate(total_apps = Count("apps") , total_follower = Count("followers")).only("first_name" , "last_name" , "username" , "image" , "bio" , "joined_at")
        return users

    def view_profile(self , username):
        try:
            return User.objects.prefetch_related(Prefetch("apps" , App.objects.filter(status = "approved")) , "jobs" , "discussions").get(username = username)
        except User.DoesNotExist:
            raise ObjectNotFound("User not found")
    
    def signup(self , user):
        return user.save()

    def edit_profile(self , user_form):
        return user_form.save()
    
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
