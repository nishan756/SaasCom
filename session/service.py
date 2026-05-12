from .repository import UserRepo , FollowRepo
from .exceptions import FollowException, InvalidForm

class UserService:
    repo = UserRepo()

    def get_user(self , id):
        return self.repo.get_user(id)

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
        