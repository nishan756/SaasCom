from .repository import AppRepo , VoteRepo , AppImageRepo , ReviewRepo
from django.utils.timezone import now
from .exceptions import AlreadyReviewed , PermissionDenied 

class AppService:
    repo = AppRepo()

    def all_apps(self , order_by = None):
        return self.repo.all_apps(order_by = order_by)
    
    def get_app(self , id):
        return self.repo.get_app(id = id)


class AppImageService:
    repo = AppImageRepo()
    def get_images(self , id):
        return self.repo.get_images(id)

class VoteService:
    repo = VoteRepo()

    def get_vote(self , app , user):
        return self.repo.get_vote(app , user)
    
    def has_vote(self , app , user):
        if user.is_authenticated:
            user_vote = self.repo.has_vote(app , user)
            if user_vote:
                if user_vote.vote_type == "upvote":
                    return "upvote"
                else:
                    return "downvote"
            return None

    def vote(self , app_id , user , vote_type):
        app = AppService().get_app(id = app_id)
        prev_vote = self.get_vote(app = app , user = user)
        if prev_vote:
            if prev_vote.vote_type != vote_type:
                prev_vote.vote_type = vote_type
                prev_vote.added_at = now()
                prev_vote.save()
                return f'Your vote updated to {vote_type}'
            else:
                prev_vote.delete()
                return f'Vote removed'
        else:
            self.repo.vote(app , user , vote_type)
            return f"Thanks for your {vote_type}"     


class ReviewService:
    repo = ReviewRepo()

    def get_review(self , id):
        return self.repo.get_review(id = id)

    def get_reviews(self , app):
        return self.repo.get_reviews(app = app)
    
    def has_user_review(self , app , user):
        return self.repo.has_user_review(app = app , user =  user)
    
    def add_review(self , app_id , user , review):
        app = AppService().get_app(id = app_id)
        prev_review = self.repo.has_user_review(app = app , user = user)
        if prev_review:
            raise AlreadyReviewed("You already reviewed on this app")
        else:
            self.repo.add_review(app , user , review)
    
    def del_review(self , id , user):
        review = ReviewService().get_review(id = id)
        if review.user != user:
            raise PermissionDenied("You can't delete this review")
        self.repo.del_review(review)


        