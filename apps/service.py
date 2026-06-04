from .repository import AppRepo , AppImageRepo , ReviewRepo
from saas_com.core.exceptions import AlreadyExists , PermissionDenied , TooManyObject , InvalidForm , InvalidPassword

class AppService:
    repo = AppRepo()

    def total_apps(self):
        return self.repo.total_apps()

    def all_apps(self , order_by = None):
        return self.repo.all_apps(order_by = order_by)
    
    def get_app(self , id):
        return self.repo.get_app(id = id)
    
    def get_app_detail(self , id):
        return self.repo.get_app_detail(id = id)
    
        
    def create_app(self , founder , form , logo):
        if form.is_valid():
            name = form.cleaned_data.get("name")
            category = form.cleaned_data.get("category")
            tags = form.cleaned_data.get("tags")
            # logo = form.cleaned_data.get("logo")
            short_description = form.cleaned_data.get("short_description")
            detail = form.cleaned_data.get("detail")
            app = self.repo.create_app(founder , name , category , tags , logo , short_description , detail)
            return app
        else:
            print(form.errors)
            raise InvalidForm("Invalid form data")

    def del_app(self, id, user, form):
        app = self.get_app(id=id)

        if app.founder != user:
            raise PermissionDenied("You can't delete this app")

        if not form.is_valid():
            raise InvalidForm("Invalid form data")

        password = form.cleaned_data.get("password")

        if not user.check_password(password):
            raise InvalidPassword("Invalid password")

        return self.repo.del_app(app)


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
    
    def del_image(self , id , founder):
        img_obj = self.get_image(id = id)
        if img_obj.app.founder == founder:
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


        