from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from rest_framework import status
from auth_app.handlers import RegisterHandler, LoginHandler, PersonalDashboardHandler, LogoutHandler
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

class RegisterView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
     
    def post(self, request):
        response = RegisterHandler.register_user(request)
        if "error" in response:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(response, status=status.HTTP_200_OK)
    
class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        response = LoginHandler.login_user(request)
        if "error" in response:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)   
        return Response(response, status=status.HTTP_200_OK)
    
class PersonalDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = PersonalDashboardHandler.get_dashboard_data(request)
        if "error" in response:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)   
        return Response(response, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        resposne = LogoutHandler.logout_user(request)
        if "error" in resposne:
            return Response(resposne, status=status.HTTP_400_BAD_REQUEST)   
        return Response(resposne, status=status.HTTP_200_OK)