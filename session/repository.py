from .models import User , Follow
from .exceptions import UserNotFound
from django.contrib.auth import authenticate

class UserRepo:
    queryset = User.objects.all()


    def get_user(self , id):
        try:
            return self.queryset.get(id = id)
        except User.DoesNotExist:
            raise UserNotFound("User not found")

    def view_profile(self , username):
        try:
            return self.queryset.prefetch_related("followers" , "following" , "apps").get(username = username)
        except User.DoesNotExist:
            raise UserNotFound("User not found")
    
    def authenticated(self , request , username , password):
        user = authenticate(request , username = username , password = password)
        if user is not None:
            return user
        raise UserNotFound("Invalid username or password")
        


class FollowRepo:
    queryset = Follow.objects.all()

    def is_following(self , follower , following):
        return self.queryset.filter(follower = follower , following = following).exists()

    def follow(self , follower , following):
        new_follow = Follow(follower = follower , following = following)
        new_follow.save()
    
    def unfollow(self , follower , following):
        follow = self.queryset.get(follower = follower , following = following)
        follow.delete()