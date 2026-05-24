from .repository import ReportRepo, UserRepo , FollowRepo , BookmarkRepo
from .exceptions import FollowException, InvalidForm , InvalidContentType
from apps.exceptions import PermissionDenied , AlreadyExists
from .models import User , Report
from apps.models import App
from jobs.models import Job
from django.contrib.contenttypes.models import ContentType


def get_content_type(content_type , valid_content_types):
    if content_type not in valid_content_types:
        raise InvalidContentType("Invalid content type")
    return ContentType.objects.get_for_model(valid_content_types[content_type])

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
        "app":App,
        "job":Job
    }

    def get_report(self , id):
        return self.repo.get_report(id = id)
    
    def get_reports(self , content_type , object_id):
        content_type = get_content_type(content_type , self.CONTENT_TYPES)
        return self.repo.get_reports(content_type , object_id)
    
    def has_user_report(self ,content_type ,  object_id , reporter):
        model = ContentType.objects.get_for_model(model = self.CONTENT_TYPES[content_type])
        return self.repo.has_user_report(content_type = model , object_id = object_id , reporter =  reporter)

    def add_report(self , reporter , content_type , id , form):

        if self.has_user_report(content_type , object_id = id , reporter = reporter):
            raise AlreadyExists("You already report on this {}".format(content_type))
        
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


class BookmarkService:
    repo = BookmarkRepo()
    CONTENT_TYPES = {
        "app" : App,
        "job":Job,
    }

    def bookmarks(self , user):
        return self.repo.bookmarks(user = user)
    
    def is_bookmarked(self , user , content_type , object_id):
        if content_type not in self.CONTENT_TYPES:
            raise InvalidContentType("Invalid content type")
        content_type = ContentType.objects.get_for_model(model = self.CONTENT_TYPES[content_type])
        return self.repo.is_bookmarked(user = user , content_type = content_type , object_id = object_id)
    
    def get_bookamark(self , user , id):
        return self.repo.get_bookamark(user , id)
    
    def add_bookmark(self , user , content_type , object_id):
        if content_type not in self.CONTENT_TYPES:
            raise InvalidContentType("you\'re trying to add invalid content type")
        
        if self.is_bookmarked(user , content_type , object_id):
            raise AlreadyExists("Already bookmarked")
        content_type = ContentType.objects.get_for_model(model = self.CONTENT_TYPES[content_type])
        return self.repo.add_bookmark(user , content_type , object_id)
    
    def delete_bookmark(self , user , id):
        bookmark = self.repo.get_bookamark(user = user , id = id)
        return self.repo.delete_bookmark(bookmark)
    

