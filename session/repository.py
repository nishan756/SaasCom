from .models import User , Follow , Report
from .exceptions import InvalidContentType, UserNotFound , ReportNotFound
from django.contrib.auth import authenticate
from django.contrib.contenttypes.models import ContentType

class UserRepo:
    queryset = User.objects.all()

    def total_user(self):
        return self.queryset.filter(is_active = True).count()


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


class ReportRepo:
    queryset = Report.objects.all()

    def get_report(self , id):
        try:
            return self.queryset.get(id = id)
        except Report.DoesNotExist:
            raise ReportNotFound("Report not found")
    
    def add_report(self , reporter , report_type , content_type , id , reason = None):
        new_report = Report(
            reporter = reporter,
            content_type = content_type,
            object_id = id,
            reason = reason if reason else None,
            report_type = report_type
        )
        new_report.save()
    
    