from .repository import VoteRepo
from apps.models import App
from .models import Vote
from saas_com.core.service import get_content_type , ContentType
from django.utils.timezone import now

class VoteService:
    repo = VoteRepo()
    CONTENT_TYPES = {
        "app":App,
    }

    def get_vote(self , user , content_type , object_id):
        content_type = get_content_type(content_type , self.CONTENT_TYPES)
        return self.repo.get_vote(user = user , content_type = content_type , object_id = object_id)

    def vote(self , user , content_type , object_id , vote_type):
        vote = self.get_vote(user , content_type , object_id)

        if vote and vote.vote_type != vote_type:
            vote.vote_type = vote_type
            vote.added_at = now()
            self.repo.vote(vote)
            return f"Your vote has updated to {vote_type}"
        
        elif vote and vote.vote_type == vote_type:
            self.repo.del_vote(vote)
            return f"Your vote has been deleted"
        
        elif not vote:
            content_type = get_content_type(content_type , self.CONTENT_TYPES)
            vote = Vote(user = user , content_type = content_type , object_id = object_id , vote_type = vote_type)
        
        self.repo.vote(vote)
        return f"Thanks for your {vote_type}"
        
        

        
        