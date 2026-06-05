from .repository import DiscussionRepo
from django.core.paginator import Paginator
from django.core.exceptions import BadRequest
from saas_com.core.exceptions import InvalidForm
from .models import Tag

class DiscussionService:
    repo = DiscussionRepo()

    def all_discussions(self , user , page , **query_set):
        supported_q_field = ["title" , "tags" , "following"]
        query_set = {key:value for key , value in query_set.items() if key in supported_q_field}
        
        if query_set.get("tags"):
            query_set["tags"] = query_set.get("tags").strip().split("#")
        
        if query_set.get("following"):
            if not user.is_authenticated:
                raise BadRequest("You must be authenticated to view discussion of your following user")

        discussions = self.repo.all_discussions(user , **query_set)

        paginator = Paginator(discussions , 20)

        discussions = paginator.get_page(page)

        return discussions
    
    def discussion_detail(self , id):
        return self.repo.discussion_detail(id = id)
    
    def get_discussion(self , author , id):
        return self.repo.get_discussion(author , id = id)

    def trending_discussions(self):
        return self.repo.trending_discussions()
    
    def post_discussion(self , author , form):
        if form.is_valid():
            author = author
            tags = form.cleaned_data.get("tags")
            title = form.cleaned_data.get("title")
            short_description = form.cleaned_data.get("short_description")
            detail = form.cleaned_data.get("detail")
            banner = form.cleaned_data.get("banner" , None)
            return self.repo.post_discussion(title , author , tags , short_description , detail , banner)
        raise InvalidForm((form.errors))
    
    def delete_discussion(self , author , id):
        discussion = self.get_discussion(author = author , id = id)
        return self.repo.delete_discussion(discussion)
    
    def update_discussion(self , form):
        if form.is_valid():
            tags = form.cleaned_data.get("tags" , None)
            return self.repo.update_discussion(form , tags)
        raise InvalidForm("Invalid form data")