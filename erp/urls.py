from django.urls import path
from erp.views import CourseEnrollmentView, CourseListView, AcademicYearView

urlpatterns = [
    path('enroll-student/', CourseEnrollmentView.as_view(), name='course-enroll'),
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('academic-years/', AcademicYearView.as_view(), name='academic-year-list'),
]