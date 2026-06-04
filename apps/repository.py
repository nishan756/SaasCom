from .models import App , AppImages , Review
from vote.models import Vote
from saas_com.core.exceptions import ObjectNotFound
from django.db.models import Count , Q , Avg

class AppRepo:
    
    def total_apps(self):
        return App.objects.filter(status = "approved").count()
    
    def all_apps(self , order_by = None):
        apps = App.objects.select_related("founder").prefetch_related(
            "category","votes"
        ).annotate(
            #Total upvotes
            total_upvote = Count("votes" , filter = Q(votes__vote_type = "upvote") , distinct = True),
            #Total Downvotes
            total_downvote = Count("votes" , filter = Q(votes__vote_type = "downvote") , distinct = True),
            # avg rating
            avg_rating = Avg("reviews__rating" , distinct= True)
        )
        return apps if not order_by else apps.order_by(order_by)
    
    def get_app(self , id):
        try:
            return App.objects.get(id = id)
        except App.DoesNotExist:
            raise ObjectNotFound("App not found")

    def get_app_detail(self , id):
        try:
            return App.objects.select_related("founder").prefetch_related("category" , "app_images" , "reviews" , "reviews__user").get(id = id)
        except App.DoesNotExist:
            raise ObjectNotFound("App not found")
        
    def create_app(self , founder , name , category , logo , short_description , detail):
        new_app = App.objects.create(
            founder = founder,
            name = name,
            logo = logo,
            short_description = short_description,
            detail = detail
        )
        new_app.category.set(category)
        return new_app
    
    def update_app(self , form , category):
        updated_app = form.save()
        updated_app.category.set(category)
        return  updated_app
    
    def del_app(self , app):
        return app.delete()

class AppImageRepo:

    def get_images(self , id):
        app = AppRepo().get_app(id = id)
        return AppImages.objects.filter(app = app)
    
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
    


class ReviewRepo:

    def get_review(self , id):
        try:
            return Review.objects.get(id = id)
        except Review.DoesNotExist:
            raise ObjectNotFound("Review not found")
    def get_reviews(self , app):
        return Review.objects.filter(app = app).select_related("user")

    def has_user_review(self ,  app , user):
        return Review.objects.filter(app = app , user = user).exists()

    def add_review(self , app , user , review , rating = None):
        Review.objects.create(
            app = app , 
            user = user,
            review = review,
            rating = rating
        )
        return

    def del_review(self , review):
        review.delete()
        return

    
    

    
    
    