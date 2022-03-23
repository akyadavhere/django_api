from django.conf import settings


from rest_framework_simplejwt.authentication import JWTAuthentication

# authenitcate() verifies and decode the token

def get_user(request):
   jwt_authenticator = JWTAuthentication()
   response = jwt_authenticator.authenticate(request)
   if response is not None:
      user, token = response
      return user
   return None