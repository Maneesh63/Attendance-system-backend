
from auth_app.models import User, BlacklistedToken, UserQR
import traceback
from auth_app.jwt_handler import generate_jwt
from django.db import IntegrityError
from django.db import transaction
from auth_app.utils import hash_password, verify_password
from auth_app.jwt_handler import decode_jwt



class RegisterHandler:
    
    @classmethod
    def register_user(cls, request):
        username = request.data.get("username", " ")
        email = request.data.get("email")
        phone = request.data.get("phone", "")
        password = request.data.get("password")
        role = request.data.get("role", "student")

        if not email:
            return {"error": "Email required"}
        
        if not password:
            return {"error": "Password required"}
        
        try:
            if User.objects.filter(email=email).exists():
                return {"error": "User already exists, try login"}

            try:
                with transaction.atomic():
                    user = User(
                        username=username or email,
                        email=email,
                        password=hash_password(password),
                        phone=phone,
                        role=role
                    )

                    # user.set_password(password)    
                    user.save()
                    token, user_id, email = generate_jwt(user)
                    print("Type Token:", type(token))
                    return {
                        "message": "User registered successfully",
                        "token": token,
                        "token_type": "Bearer",
                        "user_id": user_id,
                        "role": user.role
                    }
            
            except IntegrityError:
                return {"error": "User creation failed"}
            
        except Exception as e:
            traceback.print_exc()
            return {"error": "executing execption block for user registartion"}
        
class LoginHandler:

    @classmethod
    def login_user(cls, request):
        print("Login request data:", request.data)
        email = request.data.get("email")
        password = request.data.get("password")

        if not email:
            return {"error": "Email required"}
        
        if not password:
            return {"error": "Password required"}
        
        try:
            try:
                user = User.objects.get(email=email)
                print("user found:", user)
            except User.DoesNotExist:
                return {"error": "Invalid credentials"}

            if not verify_password(password, user.password):
                return {"error": "Invalid credentials"}
            
            token, user_id, email = generate_jwt(user)
            return {
                "message": "Login successful",
                "token": token,
                "token_type": "Bearer",
                "user_id": user_id,
                "role": user.role
            }
        
        except Exception as e:
            traceback.print_exc()
            return {"error": "executing exception block for user login"}
        
class LogoutHandler:

    def logout_user(cls, request):
        
        auth = request.headers.get("Authorization")
        print("auth header:", auth)
        token = auth.split()[1]
        print("token to be blacklisted:", token)
        
        try:
            payload = decode_jwt(token)
            BlacklistedToken.objects.create(jti=payload["jti"])
            return {"message": "Logout successful"}
        
        except Exception as e:
            traceback.print_exc()
            return {"error": "Error during logout"}


class PersonalDashboardHandler:
    
    @classmethod
    def get_dashboard_data(cls, request):
        user = request.user
        user_id = user.user_id
        print("user_id", user_id)
        print("request user:", user)

        user_qr = UserQR.objects.filter(user__user_id=user_id, is_active=True).first()
        if user_qr:
            print("User QR found:", user_qr.qr_code_url)
        try:
            print("user in handler:", user)
            data = {
                "message": f"Welcome to your dashboard, {user.username}!",
                "email": user.email,
                "role": user.role,
                "username": user.username,
                "qr_code_url": user_qr.qr_code_url if user_qr else None
            }
            return data
        except Exception as e:
            traceback.print_exc()
            return {"error": "Error fetching dashboard data"}
        
