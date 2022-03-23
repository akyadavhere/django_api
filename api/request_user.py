from rest_framework_simplejwt.authentication import JWTAuthentication
JWT_authenticator = JWTAuthentication()

# authenitcate() verifies and decode the token
# if token is invalid, it raises an exception and returns 401

def get_user(request):
   response = JWT_authenticator.authenticate(request)
   if response is not None:
      # unpacking
      user , token = response
      print("this is decoded token claims", token.payload)
      print("this is user id",user)
      return user
   else:
      print("no token is provided in the header or the header is missing")
      return None