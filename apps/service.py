from .repository import AppRepo , AppImageRepo , ReviewRepo
from saas_com.core.exceptions import AlreadyExists , PermissionDenied , TooManyObject , InvalidForm , InvalidPassword
from django.core.paginator import Paginator

class AppService:
    repo = AppRepo()

    def total_apps(self):
        return self.repo.total_apps()

    def all_apps(self, page, **query_set):

        # Order by safely
        order_by = query_set.pop("order_by", "new")

        ordering_fields = {
            "new": "-added_at",
            "old": "added_at",
            "less_rated": "avg_rating",
            "top_rated": "-avg_rating"
        }

        order_by = ordering_fields.get(order_by)

        # Filter only supported fields
        supported_q_field = ["name", "category"]
        query_set = {
            key: value
            for key, value in query_set.items()
            if key in supported_q_field
        }

        # Query
        apps = self.repo.all_apps(order_by=order_by, **query_set)

        # Pagination
        paginator = Paginator(apps, 20)
        apps = paginator.get_page(int(page))

        return apps
    
    def get_app(self , id):
        return self.repo.get_app(id = id)
    
    def get_app_detail(self , id):
        return self.repo.get_app_detail(id = id)
    
    def trending_apps(self):
        return self.repo.trending_apps()
    
        
    def create_app(self , user , form):
        app_credentials = form.cleaned_data.copy()
        app_credentials["user"] = user
        category = app_credentials.pop("category" , [])
        return self.repo.create_app(category , **app_credentials)
    
    def update_app(self , form):
        category = form.cleaned_data.get("category")
        return self.repo.update_app(form , category)

    def del_app(self, id, user, form):
        app = self.get_app(id=id)

        if app.user != user:
            raise PermissionDenied("You can't delete this app")

        if not form.is_valid():
            raise InvalidForm("Invalid form data")

        password = form.cleaned_data.get("password")

        if not user.check_password(password):
            raise InvalidPassword("Invalid password")

        return self.repo.del_app(app)
    
    def get_user_apps(self , user):
        return self.repo.get_user_apps(user)

class AppImageService:
    repo = AppImageRepo()
    def get_app_images(self , id):
        return self.repo.get_images(id)
    
    def get_image(self , id):
        return self.repo.get_image(id)
    
    def add_images(self , app , images):
        if len(images) > 5:
            raise TooManyObject("Maximum 5 image is allowed")
        return self.repo.add_images(app , images)
    
    def del_image(self , id , user):
        img_obj = self.get_image(id = id)
        if img_obj.app.user == user:
            return self.repo.del_image(img_obj)
        raise PermissionDenied("You can\'t delete this image")     


class ReviewService:
    repo = ReviewRepo()

    def get_review(self , id):
        return self.repo.get_review(id = id)

    def get_reviews(self , app):
        return self.repo.get_reviews(app = app)
    
    def has_user_review(self , app , user):
        return self.repo.has_user_review(app = app , user =  user)
    
    def add_review(self , app_id , user , review , rating = None):
        app = AppService().get_app(id = app_id)
        if app.user == user:
            raise PermissionDenied("You can't review on your app")
        prev_review = self.repo.has_user_review(app = app , user = user)
        if prev_review:
            raise AlreadyExists("You already reviewed on this app")
        else:
            self.repo.add_review(app , user , review , rating)        
    
    def del_review(self , id , user):
        review = ReviewService().get_review(id = id)
        if review.user != user:
            raise PermissionDenied("You can't delete this review")
        self.repo.del_review(review)


        