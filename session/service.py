from .repository import ReportRepo, UserRepo , FollowRepo
from .exceptions import FollowException, InvalidForm , InvalidContentType
from .models import User
from apps.models import App
from django.contrib.contenttypes.models import ContentType

class UserService:
    repo = UserRepo()

    def total_user(self):
        return self.repo.total_user()

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

class ReportService:
    repo = ReportRepo()
    CONTENT_TYPES = {
        "user":User,
        "app":App
    }


    def add_report(self , reporter , content_type , id , form):
        if content_type not in self.CONTENT_TYPES:
            raise InvalidContentType("Invalid content type.")
        content_type = ContentType.objects.get_for_model(model = self.CONTENT_TYPES[content_type])
        if form.is_valid():
            reason = form.cleaned_data.get("reason" , None)
            report_type = form.cleaned_data.get("report_type")
            return self.repo.add_report(reporter = reporter, content_type = content_type, id = id, reason = reason , report_type = report_type)
        raise InvalidForm("Invalid form data.")
    