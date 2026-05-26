from .repository import UserRepo , FollowRepo , BookmarkRepo
from saas_com.core.exceptions import AlreadyExists , FollowException, InvalidForm , InvalidContentType
from apps.models import App
from jobs.models import Job
from saas_com.core.service import get_content_type

class UserService:
    repo = UserRepo()

    def total_user(self):
        return self.repo.total_user()

    def get_user(self , id):
        return self.repo.get_user(id)
    
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


class BookmarkService:
    repo = BookmarkRepo()
    CONTENT_TYPES = {
        "app" : App,
        "job":Job,
    }

    def bookmarks(self , user):
        return self.repo.bookmarks(user = user)
    
    def is_bookmarked(self , user , content_type , object_id):
        content_type = get_content_type(content_type , self.CONTENT_TYPES)
        return self.repo.is_bookmarked(user = user , content_type = content_type , object_id = object_id)
    
    def get_bookamark(self , user , id):
        return self.repo.get_bookamark(user , id)
    
    def add_bookmark(self , user , content_type , object_id):
        content_type = get_content_type(content_type , self.CONTENT_TYPES)
        if self.is_bookmarked(user , content_type , object_id):
            raise AlreadyExists("Already bookmarked")
        return self.repo.add_bookmark(user , content_type , object_id)
    
    def delete_bookmark(self , user , id):
        bookmark = self.repo.get_bookamark(user = user , id = id)
        return self.repo.delete_bookmark(bookmark)
    

