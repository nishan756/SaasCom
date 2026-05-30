from .models import Discussion
from django.db.models import Count
from session.models import Follow
from saas_com.core.exceptions import ObjectNotFound

class DiscussionRepo:

    def all_discussions(self, user, **query_set):
        
        discussions = Discussion.objects.select_related("author").prefetch_related(
        "tags" , "votes").annotate(total_vote=Count("votes"))
        if query_set.get("title"):
            discussions = discussions.filter(
                title__icontains=query_set["title"]
            )

        if query_set.get("tags"):
            discussions = discussions.filter(
                tags__title__in=query_set["tags"]
            )

        if query_set.get("following"):

            following = list(Follow.objects.filter(follower = user).values_list("following__username" , flat = True))

            discussions = discussions.filter(author__username__in = following)

        return discussions
    
    def discussion_detail(self , id):
        try:
            return Discussion.objects.select_related("author").prefetch_related("tags").get(id = id)
        except Discussion.DoesNotExist:
            raise ObjectNotFound("Discussion not found")
    