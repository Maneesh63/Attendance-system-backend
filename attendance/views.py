from rest_framework.views import APIView
from attendance.handler import AttendanceHandler
from rest_framework.response import Response
from rest_framework import status

class CreateAttendanceView(APIView):
      
    def post(self, request):
        response = AttendanceHandler.create_user_qr(request)
        if "error" in response:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)   
        return Response(response, status=status.HTTP_200_OK)
    

class MarkAttendanceView(APIView):

    def post(self, request):
        response = AttendanceHandler.mark_attendance(request)
        if "error" in response:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(response, status=status.HTTP_200_OK)
           