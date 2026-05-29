from .repository import BookmarkRepo

# ==============MODELS=============
from apps.models import App
from jobs.models import Job

# ==============GenericPrograms=====
from saas_com.core.service import get_content_type
from saas_com.core.exceptions import AlreadyExists


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
        if self.is_bookmarked(user , content_type , object_id):
            raise AlreadyExists("Already bookmarked")
        content_type = get_content_type(content_type , self.CONTENT_TYPES)
        return self.repo.add_bookmark(user , content_type , object_id)
    
    def delete_bookmark(self , user , id):
        bookmark = self.repo.get_bookamark(user = user , id = id)
        return self.repo.delete_bookmark(bookmark)