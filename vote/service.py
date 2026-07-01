from .repository import VoteRepo
from apps.models import App
from discussion.models import Discussion
from .models import Vote
from saas_com.core.service import get_content_type
from django.utils.timezone import now
from saas_com.core.exceptions import PermissionDenied

class VoteService:
    repo = VoteRepo()
    CONTENT_TYPES = {
        "app":App,
        "discussion":Discussion,
    }

    def get_vote(self , user , content_type_str , object_id):
        content_type_obj = get_content_type(content_type_str , self.CONTENT_TYPES)
        return self.repo.get_vote(user = user , content_type = content_type_obj , object_id = object_id)

    def vote(self , user , content_type_str , object_id , vote_type):
        
        if self.CONTENT_TYPES[content_type_str].objects.filter(id = object_id , user = user).exists():

            raise PermissionDenied(f"You can't vote on your {content_type_str}")
        
        vote = self.get_vote(user , content_type_str , object_id)

        if vote and vote.vote_type != vote_type:
            vote.vote_type = vote_type
            vote.added_at = now()
            self.repo.vote(vote)
            return f"Your vote has updated to {vote_type}"
        
        elif vote and vote.vote_type == vote_type:
            self.repo.del_vote(vote)
            return f"Your vote has been deleted"
        
        elif not vote:
            content_type_obj = get_content_type(content_type_str , self.CONTENT_TYPES)
            vote = Vote(user = user , content_type = content_type_obj , object_id = object_id , vote_type = vote_type)
        
        self.repo.vote(vote)
        return f"Thanks for your {vote_type}"
    
    def get_object_votes_stats(self , content_type_str , object_id , **query_param):
        supporter_query_param = ["date_from" , "date_to"]
        query_param = {key:value for key , value in query_param.items() if key in supporter_query_param}

        content_type_obj = get_content_type(content_type_str , self.CONTENT_TYPES)

        stats =  self.repo.get_object_votes_stats(content_type_obj , object_id , **query_param)

        stats["upvote_ratio"] = f"{round(stats["total_upvote"]*100 / stats["total_vote"] if stats["total_vote"] > 0 else 0 , 2)}%"

        stats["downvote_ratio"] = f"{round(stats["total_downvote"]*100 / stats["total_vote"] , 2) if stats["total_vote"] > 0 else 0 }%"

        stats["vote_score"] = stats["total_upvote"] - stats["total_downvote"]

        return stats