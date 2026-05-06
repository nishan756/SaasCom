from .models import User , Follow
from .exceptions import UserNotFound
from django.contrib.auth import authenticate

class UserRepo:
    queryset = User.objects.all()

    def view_profile(self , username):
        try:
            return self.queryset.prefetch_related("followers" , "following").get(username = username)
        except User.DoesNotExist:
            raise UserNotFound("User not found")
    
    def authenticated(self , request , username , password):
        user = authenticate(request , username = username , password = password)
        if user is not None:
            return user
        raise UserNotFound("Invalid username or password")
        
    def add_follower(self , following , follower):
        pass

    def remove_follower(self , following , follower):
        pass
    
    

