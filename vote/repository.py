from .models import Vote

class VoteRepo:

    def get_vote(self , user , content_type , object_id):
        return Vote.objects.filter(user = user , content_type = content_type , object_id = object_id).first()

    def vote(self , vote):
        vote.save()
    
    def del_vote(self , vote):
        vote.delete()