from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from rest_framework import status
from erp.handlers import CourseEnrollmentHandler
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny


class CourseEnrollmentView(APIView):

    def post(self, request):
        response = CourseEnrollmentHandler.enroll_student(request)
        if "error" in response:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)   
        return Response(response, status=status.HTTP_200_OK)
    
    def get(self, request):
        response = CourseEnrollmentHandler.get_enrollments(request)
        if "error" in response:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)   
        return Response(response, status=status.HTTP_200_OK)
    

class CourseListView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        response = CourseEnrollmentHandler.list_courses(request)
        if "error" in response:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)   
        return Response(response, status=status.HTTP_200_OK)
    

class AcademicYearView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        response = CourseEnrollmentHandler.list_academic_years(request)
        if "error" in response:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)   
        return Response(response, status=status.HTTP_200_OK)
    
