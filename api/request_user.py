from rest_framework_simplejwt.authentication import JWTAuthentication

def get_user(request):
   jwt_authenticator = JWTAuthentication()
   response = jwt_authenticator.authenticate(request) #verify and decode
   if response is not None:
      user, token = response
      return user
   return None
