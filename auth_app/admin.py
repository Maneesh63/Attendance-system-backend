from django.contrib import admin
from auth_app.models import User, UserQR

# Register your models here.
admin.site.register(User)
admin.site.register(UserQR)