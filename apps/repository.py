from .models import App , AppImages , AppVote , Review
from .exceptions import AppNotFound , ReviewNotFound
from session.exceptions import UserNotFound
from django.db.models import Prefetch
from django.db.models import Count , Q
from .models import User
from django.utils.timezone import now

class AppRepo:
    queryset = App.objects.all()
    
    def total_apps(self):
        return self.queryset.count()
    
    def all_apps(self , order_by = None):
        apps = self.queryset.prefetch_related(
            "category",
            Prefetch(
                lookup = "app_votes",
                queryset = AppVote.objects.all()
            )
        ).annotate(
            #Total upvotes
            total_upvote = Count("app_votes" , filter = Q(app_votes__vote_type = "upvote")),
            #Total Downvotes
            total_downvote = Count("app_votes" , filter = Q(app_votes__vote_type = "downvote"))
        )
        return apps if not order_by else apps.order_by(order_by)
    
    def get_app(self , id):
        try:
            return App.objects.get(id = id)
        except App.DoesNotExist:
            raise AppNotFound("App not found")


class AppImageRepo:
    queryset = AppImages.objects.all()

    def get_images(self , id):
        app = AppRepo().get_app(id = id)
        return self.queryset.filter(app = app)
    
    

class VoteRepo:
    queryset = AppVote.objects.all()


    def get_vote(self , app , user):
        try:
            return self.queryset.get(app = app , user = user)
        except  AppVote.DoesNotExist:
            return None
    
    def has_vote(self , app , user):
        return AppVote.objects.filter(app = app , user = user).first()

    def vote(self , app , user , vote_type):
        new_vote = AppVote(app = app , user = user , vote_type = vote_type)
        new_vote.save()
        return


class ReviewRepo:
    queryset = Review.objects.all()

    def get_review(self , id):
        try:
            return Review.objects.get(id = id)
        except Review.DoesNotExist:
            raise ReviewNotFound("Review not found")
    def get_reviews(self , app):
        return self.queryset.filter(app = app).select_related("user")

    def has_user_review(self ,  app , user):
        return self.queryset.filter(app = app , user = user).exists()

    def add_review(self , app , user , review):
        Review.objects.create(
            app = app , 
            user = user,
            review = review
        )
        return

    def del_review(self , review):
        review.delete()
        return

    
    

    
    
    