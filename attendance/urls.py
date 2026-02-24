from rest_framework.urls import urlpatterns
from django.urls import path
from attendance.views import CreateAttendanceView, MarkAttendanceView

urlpatterns = [
    path('create-attendance/', CreateAttendanceView.as_view(), name='create-attendance'),
    path('mark-attendance/', MarkAttendanceView.as_view(), name='mark-attendance'),

]