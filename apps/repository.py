from .models import App , AppImages , AppVote , Review
from saas_com.core.exceptions import ObjectNotFound
from django.db.models import Prefetch
from django.db.models import Count , Q

class AppRepo:
    queryset = App.objects.all()
    
    def total_apps(self):
        return self.queryset.filter(status = "approved").count()
    
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
            raise ObjectNotFound("App not found")

    def get_app_detail(self , id):
        try:
            return App.objects.select_related("founder").prefetch_related("category" , "tags" , "app_images" , "reviews" , "reviews__user").get(id = id)
        except App.DoesNotExist:
            raise ObjectNotFound("App not found")
        
    def create_app(self , founder , name , category , tags , logo , short_description , detail):
        new_app = App.objects.create(
            founder = founder,
            name = name,
            logo = logo,
            short_description = short_description,
            detail = detail
        )
        new_app.category.set(category)
        new_app.tags.set(tags)
        return new_app
    
    def del_app(self , app):
        return app.delete()

class AppImageRepo:
    queryset = AppImages.objects.all()

    def get_images(self , id):
        app = AppRepo().get_app(id = id)
        return self.queryset.filter(app = app)
    
    def get_image(self , id):
        try:
            return AppImages.objects.get(id = id)
        except AppImages.DoesNotExist:
            raise ObjectNotFound("Image not found")
    
    def add_images(self , app , images):
        for image in images:
            AppImages.objects.create(
                app = app , 
                image = image
            )
        return
    
    def del_image(self , img_obj):
        img_obj.delete()
    
    
    

class VoteRepo:
    queryset = AppVote.objects.all()


    def get_vote(self , app , user):
        try:
            return self.queryset.get(app = app , user = user)
        except  AppVote.DoesNotExist:
            return None
    
    def has_vote(self , app , user):
        return AppVote.objects.filter(app = app , user = user).only("vote_type").first()

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
            raise ObjectNotFound("Review not found")
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

    
    

    
    
    