from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header
from user.models import CustomUser
import jwt

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request): # it will return user object
        try:
            token = get_authorization_header(request).decode('utf-8')
            if token is None or token == "null" or token.strip() == "":
                raise exceptions.AuthenticationFailed('Authorization Header or Token is missing on Request Headers')
            print("printed by custom_auth",token)
            decoded = jwt.decode(token, settings.SECRET_KEY)
            email = decoded['email']
            user_obj = CustomUser.objects.get(email=email)
        except jwt.ExpiredSignatureError:
            print("reach")

            raise exceptions.AuthenticationFailed('Token Expired, Please Login')

        except jwt.DecodeError :
            print("reach")

            raise exceptions.AuthenticationFailed('Token Modified by thirdparty')
        except jwt.InvalidTokenError:
            print("reach")

            raise exceptions.AuthenticationFailed('Invalid Token')
        except Exception as e:
            print("reach")

            raise exceptions.AuthenticationFailed(e)
        print("reached")
        return (user_obj, None)

    def get_user(self, userid):
        try:
            return CustomUser.objects.get(id=userid)
        except Exception as e:
            return None