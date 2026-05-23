from .models import User , Follow , Report , Bookmark
from .exceptions import ReportNotFound
from apps.exceptions import ObjectNotFound
from django.contrib.auth import authenticate

class UserRepo:

    def total_user(self):
        return User.objects.filter(is_active = True).count()

    def get_user(self , id):
        try:
            return User.objects.get(id = id)
        except User.DoesNotExist:
            raise ObjectNotFound("User not found")
    
    def get_users(self , user_type):
        return User.objects.prefetch_related("apps" , "followers" , "following").filter(user_type = user_type)

    def view_profile(self , username):
        try:
            return User.objects.prefetch_related("followers" , "following" , "apps").get(username = username)
        except User.DoesNotExist:
            raise ObjectNotFound("User not found")
    
    def authenticated(self , request , username , password):
        user = authenticate(request , username = username , password = password)
        if user is not None:
            return user
        raise ObjectNotFound("Invalid username or password")
        


class FollowRepo:

    def is_following(self , follower , following):
        return Follow.objects.filter(follower = follower , following = following).exists()

    def follow(self , follower , following):
        new_follow = Follow(follower = follower , following = following)
        new_follow.save()
    
    def unfollow(self , follower , following):
        follow = Follow.objects.get(follower = follower , following = following)
        follow.delete()


class ReportRepo:

    def get_report(self , id):
        try:
            return Report.objects.get(id = id)
        except Report.DoesNotExist:
            raise ReportNotFound("Report not found")
    
    def has_user_report(self ,content_type , object_id , reporter):
        return Report.objects.filter(content_type = content_type , reporter = reporter , object_id = object_id).exists()
    
    def add_report(self , reporter , report_type , content_type , id , reason = None):
        new_report = Report(
            reporter = reporter,
            content_type = content_type,
            object_id = id,
            reason = reason if reason else None,
            report_type = report_type
        )
        new_report.save()
    
    def del_report(self , report):
        report.delete()
    

class BookmarkRepo:

    def bookmarks(self , user):
        return Bookmark.objects.filter(user = user)

    def is_bookmarked(self , user , content_type , object_id):
        return Bookmark.objects.filter(user = user , content_type = content_type , object_id = object_id).first()
    
    def get_bookamark(self , user , id):
        try:
            return Bookmark.objects.get(user = user , id = id)
        except Bookmark.DoesNotExist:
            raise ObjectNotFound("Bookmark not found")
    
    def add_bookmark(self , user , content_type , object_id):
        return Bookmark.objects.create(user = user , content_type = content_type , object_id = object_id)
    
    def delete_bookmark(self , bookmark):
        return bookmark.delete()