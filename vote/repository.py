from .models import Vote
from django.db.models import Count , Q

class VoteRepo:

    def get_vote(self , user , content_type , object_id):
        return Vote.objects.filter(user = user , content_type = content_type , object_id = object_id).first()

    def vote(self , vote):
        vote.save()
    
    def del_vote(self , vote):
        vote.delete()
    
    def get_object_votes_stats(self , content_type , object_id , **query_param):
        votes = Vote.objects.filter(content_type = content_type , object_id = object_id)

        date_from = query_param.get("date_from" , None)
        date_to = query_param.get("date_to" , None)

        if date_from and date_to:
            votes = votes.filter(added_at__date__gte = date_from , added_at__lte = date_to)
        
        elif date_from:
            votes = votes.filter(added_at__date__gte = date_from)
        
        elif date_to:
            votes = votes.filter(added_at__date__lte = date_to)

        stats = votes.aggregate(
            total_upvote = Count("id" , filter = Q(vote_type = "upvote")),
            total_downvote = Count("id" , filter = Q(vote_type = "downvote")),
        )

        return {"total_upvote":stats["total_upvote"] , "total_downvote":stats["total_downvote"]}