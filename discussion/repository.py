from .models import Discussion
from django.db.models import Count
from session.models import Follow
from saas_com.core.exceptions import ObjectNotFound
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count , F , Subquery , Prefetch , OuterRef
from django.db.models.functions import Coalesce
from vote.models import Vote
from comment.models import Comment
from django.contrib.contenttypes.models import ContentType

class DiscussionRepo:

    def all_discussions(self, user, **query_set):
        
        discussions = Discussion.objects.select_related("author").prefetch_related(
        "tags" , "votes").annotate(total_vote=Count("votes")).order_by("-posted_at")
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
    
    def get_discussion(self , author , id):
        try:
            return Discussion.objects.get(author = author , id = id)
        except Discussion.DoesNotExist:
            raise ObjectNotFound("Discussion not found")
    
    def discussion_detail(self , id):
        try:
            return Discussion.objects.select_related("author").prefetch_related("tags").get(id = id)
        except Discussion.DoesNotExist:
            raise ObjectNotFound("Discussion not found")
    
    def trending_discussions(self):
        last_seven_days = timezone.now() - timedelta(days=7)

        discussion_content_type = ContentType.objects.get_for_model(Discussion)

        vote_subquery = Vote.objects.filter(
            added_at__gte=last_seven_days,
            object_id=OuterRef("id"),
            content_type=discussion_content_type
        ).values("object_id").annotate(
            vote_count=Count("id")
        ).values("vote_count")[:1]

        comment_subquery = Comment.objects.filter(
            posted_at__gte=last_seven_days,
            object_id=OuterRef("id"),
            content_type=discussion_content_type
        ).values("object_id").annotate(
            comment_count=Count("id")
        ).values("comment_count")[:1]

        discussions = Discussion.objects.annotate(
            vote_score=Coalesce(Subquery(vote_subquery), 0),
            comment_score=Coalesce(Subquery(comment_subquery), 0),
        ).annotate(
            trending_score=F("vote_score") + (F("comment_score") * 1.5)
        ).order_by("-trending_score")

        return discussions
        
    def post_discussion(self ,title , author , tags , short_description , detail , banner):
        discussion = Discussion.objects.create(title = title , author = author , banner = banner , short_description = short_description , detail = detail)
        discussion.tags.set(tags)
        return discussion
    
    def delete_discussion(self , discussion):
        return discussion.delete()
    
    def update_discussion(self , form , tags):
        updated_discussion = form.save()
        updated_discussion.tags.set(tags)
        return updated_discussion
