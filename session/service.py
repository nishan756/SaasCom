from .repository import UserRepo
from .exceptions import InvalidForm

class UserService:
    repo = UserRepo()

    def authenticated(self , form , request):
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            return self.repo.authenticated(request, username, password)
        raise InvalidForm("Invalid form data")