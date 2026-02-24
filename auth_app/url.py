from auth_app.views import RegisterView, LoginView, PersonalDashboardView
from django.urls import path

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('dashboard/', PersonalDashboardView.as_view(), name='dashboard'),
]