from .models import User , Follow
from .exceptions import UserNotFound

class UserRepo:
    queryset = User.objects.all()

    def view_profile(self , username):
        try:
            return self.queryset.prefetch_related("followers" , "following").get(username = username)
        except User.DoesNotExist:
            raise UserNotFound("User not found")
        
    def add_follower(self , following , follower):
        pass

    def remove_follower(self , following , follower):
        pass
    
    

