from .repository import UserRepo , FollowRepo
from saas_com.core.exceptions import FollowException, InvalidForm , InvalidContentType

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

    

