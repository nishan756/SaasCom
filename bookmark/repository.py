from .models import Bookmark
from saas_com.core.exceptions import ObjectNotFound

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

