from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from auth_app.models import User, BlacklistedToken

ALGORITHM = "HS256"
class JWTAuthentication(BaseAuthentication):
    # EXCLUDED_PATHS = ["/auth/register/", "/auth/login/"]

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        
        # if any(request.path.startswith(path) for path in self.EXCLUDED_PATHS):
        #     return None
        
        if not auth_header:
            raise AuthenticationFailed("Authentication credentials were not provided")
        
        try:
            prefix, token = auth_header.split()
            if prefix.lower() != "bearer":
                raise AuthenticationFailed("Invalid token prefix")
            
        except ValueError:
            raise AuthenticationFailed("Invalid Authorization header format")
        
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=ALGORITHM
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")
        
        # if BlacklistedToken.objects.filter(jti=payload["jti"]).exists():
        #     raise AuthenticationFailed("Token has been logged out")
        
        user_id = payload.get("user_id")
        if not user_id:
            raise AuthenticationFailed("Invalid payload")
        
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found")

        return (user, token)  