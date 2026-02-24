from django.db import models
import uuid
# Create your models here.



class DateAbstract(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    
    class Meta:
        abstract = True


class User(DateAbstract):
    
    STUDENT = "student"
    ADMIN = "admin"
    TEACHER = "teacher"
    

    ROLE_TYPES = [
        (STUDENT, "Student"),
        (TEACHER, "Teacher"),
        (ADMIN, "Admin"),
    ]

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    password = models.CharField(max_length=128)
    role = models.CharField(choices=ROLE_TYPES, default=STUDENT, max_length=20)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
    
    @property
    def is_authenticated(self):
        return True
    
class BlacklistedToken(models.Model):
    jti = models.CharField(max_length=36, unique=True) # JWT ID
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.jti
    
class UserQR(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    qr_token = models.TextField(unique=True)
    qr_image = models.ImageField(upload_to="user_qr/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)