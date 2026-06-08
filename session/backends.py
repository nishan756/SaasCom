from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend:

    def authenticate(self , request , username = None , password = None):
        
        if username == None or password == None:
            return None
        
        try:
            user = User.objects.get(email = username)
            
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None
    
    def get_user(self , id):

        try:
            return User.objects.get(id = id)

        except User.DoesNotExist:
            return None