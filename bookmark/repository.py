from .models import Bookmark
from saas_com.core.exceptions import ObjectNotFound

class BookmarkRepo:

    def bookmarks(self , user , content_type):
        return Bookmark.objects.filter(user = user , content_type = content_type)

    def is_bookmarked(self , user , content_type , object_id):
        return Bookmark.objects.filter(user = user , content_type = content_type , object_id = object_id).first()
    
    def get_bookamark(self , user , id):
        try:
            return Bookmark.objects.get(user = user , id = id)
        except Bookmark.DoesNotExist:
            raise ObjectNotFound("Bookmark not found")
    
    def get_object_bookmarks(self , content_type , object_id , **query_param):

        bookmarks = Bookmark.objects.filter(content_type = content_type , object_id = object_id)
        date_from = query_param.get("date_from" , None)
        date_to = query_param.get("date_to" , None)
        
        if date_from and date_to:
            bookmarks = bookmarks.filter(bookmarked_at__gte = date_from , bookmarked_at__lte = date_to)
        
        elif date_from:
            bookmarks = bookmarks.filter(bookmarked_at__gte = date_from)

        elif date_to:
            bookmarks = bookmarks.filter(bookmarked_at__lte = date_to)
        
        return bookmarks
    
    def add_bookmark(self , user , content_type , object_id):
        return Bookmark.objects.create(user = user , content_type = content_type , object_id = object_id)
    
    def delete_bookmark(self , bookmark):
        return bookmark.delete()

