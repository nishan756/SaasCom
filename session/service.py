from .repository import ReportRepo, UserRepo , FollowRepo
from .exceptions import FollowException, InvalidForm , InvalidContentType
from apps.exceptions import PermissionDenied
from .models import User
from apps.models import App
from django.contrib.contenttypes.models import ContentType

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

class ReportService:
    repo = ReportRepo()
    CONTENT_TYPES = {
        "user":User,
        "app":App
    }

    def get_report(self , id):
        return self.repo.get_report(id = id)
    
    def has_user_report(self ,content_type ,  object_id , reporter):
        model = ContentType.objects.get_for_model(model = self.CONTENT_TYPES[content_type])
        return self.repo.has_user_report(content_type = model , object_id = object_id , reporter =  reporter)

    def add_report(self , reporter , content_type , id , form):
        if content_type not in self.CONTENT_TYPES:
            raise InvalidContentType("Invalid content type.")
        content_type = ContentType.objects.get_for_model(model = self.CONTENT_TYPES[content_type])
        if form.is_valid():
            reason = form.cleaned_data.get("reason" , None)
            report_type = form.cleaned_data.get("report_type")
            return self.repo.add_report(reporter = reporter, content_type = content_type, id = id, reason = reason , report_type = report_type)
        raise InvalidForm("Invalid form data.")
    
    def del_report(self , id , user):
        report = self.get_report(id = id)
        if report.reporter == user:
            return self.repo.del_report(report)
        raise PermissionDenied("You can\'t delete this report")
        