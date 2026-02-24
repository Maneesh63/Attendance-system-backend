from django.contrib import admin
from erp.models import Course, Enrollment, AcademicYear, Semester, StudentSemester, StudentData, PreviousAcademicRecord

admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(AcademicYear)
admin.site.register(Semester)
admin.site.register(StudentSemester)
admin.site.register(StudentData)
admin.site.register(PreviousAcademicRecord)

# Register your models here.
