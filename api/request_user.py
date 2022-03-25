
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
# authenitcate() verifies and decode the token

def get_user(request):
   jwt_authenticator = JWTAuthentication()
   response = jwt_authenticator.authenticate(request)
   if response is not None:
      user, token = response
      return user
   return AuthenticationFailed()
   # return None