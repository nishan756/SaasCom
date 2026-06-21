from .models import App , AppImages , Review
from vote.models import Vote
from saas_com.core.exceptions import ObjectNotFound
from django.db.models import Count , Q , Avg , F , Prefetch , Sum , FloatField , Subquery , OuterRef
from django.db.models.functions import Coalesce
from datetime import timedelta
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

class AppRepo:
    
    def total_apps(self):
        return App.objects.filter(status = "approved").count()
    
    def all_apps(self , order_by = None , **query_set):
        apps = App.objects.filter(status = "approved").select_related("user").prefetch_related(
            "category","votes"
        ).annotate(
            #Total upvotes
            total_upvote = Count("votes" , filter = Q(votes__vote_type = "upvote") , distinct = True),
            #Total Downvotes
            total_downvote = Count("votes" , filter = Q(votes__vote_type = "downvote") , distinct = True),
            # avg rating
            avg_rating = Avg("reviews__rating" , distinct= True)
        )
        if query_set.get("name"):
            apps = apps.filter(
                name__icontains=query_set["name"]
            )

        if query_set.get("category"):
            apps = apps.filter(
                category__name = query_set["category"]
            )

        if order_by:
            apps = apps.order_by(order_by)

        return apps
    
    def get_app(self , id):
        try:
            return App.objects.select_related("user").get(id = id)
        except App.DoesNotExist:
            raise ObjectNotFound("App not found")

    def get_app_detail(self , id):
        try:
            return App.objects.select_related("user").prefetch_related("category" , "app_images" , "reviews" , "reviews__user").get(id = id)
        except App.DoesNotExist:
            raise ObjectNotFound("App not found")
        
    def create_app(self , category ,  **app_credentials):
        new_app = App.objects.create(
            **app_credentials
        )
        if category:
            new_app.category.set(category)
        return new_app
    
    def update_app(self , form , category):
        updated_app = form.save()
        updated_app.category.set(category)
        return  updated_app
    
    def del_app(self , app):
        return app.delete()
    
    def trending_apps(self):
        last_seven_days = timezone.now() - timedelta(days=7)

        app_content_type = ContentType.objects.get_for_model(App)

        vote_subquery = Vote.objects.filter(
            content_type=app_content_type,
            object_id=OuterRef('id'),
            added_at__gte=last_seven_days
        ).values('object_id').annotate(
            cnt=Count('id')
        ).values('cnt')[:1]

        review_subquery = Review.objects.filter(
            app=OuterRef('id'),
            added_at__gte=last_seven_days
        ).values('app').annotate(
            total_rating=Sum('rating')
        ).values('total_rating')[:1]

        apps = App.objects.filter(status="approved").annotate(
            vote_score=Coalesce(Subquery(vote_subquery), 0),
            review_rating_sum=Coalesce(Subquery(review_subquery), 0.0, output_field=FloatField())
        ).annotate(
            trending_score=F("vote_score") + (F("review_rating_sum") * 1.5)
        ).order_by("-trending_score")

        return apps
    
    
    def get_user_apps(self , user):

        apps = App.objects.filter(user = user).select_related("user")
        
        apps_count = apps.aggregate(
            total_pending_apps = Count("id" , filter = Q(status = "pending")),
            total_rejected_apps = Count("id" , filter = Q(status = "rejected")),
        )

        return {"apps":apps , "total_pending_apps":apps_count["total_pending_apps"] , "total_rejected_apps":apps_count["total_rejected_apps"]}

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
    
    def get_app_rating_stats(self , app , **query_param):
        reviews = Review.objects.filter(app = app)
        date_from = query_param.get("date_from" , None)
        date_to = query_param.get("date_to" , None)

        if date_from and date_to:
            reviews = reviews.filter(added_at__gte = date_from , added_at__lte = date_to)
        
        elif date_from:
            reviews = reviews.filter(added_at__gte = date_from)
        
        elif date_to:
            reviews = reviews.filter(added_at__lte = date_to)
        
        rating_stats = reviews.aggregate(
            avg_rating = Avg("rating")
        )

        return rating_stats["avg_rating"]
    
    

    
    
    