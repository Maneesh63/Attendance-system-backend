from django.db import models
from auth_app.models import DateAbstract, User



class Course(DateAbstract):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    total_years = models.CharField(max_length=10)
    total_semesters = models.CharField(max_length=10)
    total_credits = models.CharField(max_length=10, null=True, blank=True)
    is_active = models.BooleanField(default=True)
     
    def __str__(self):
        return self.name

class AcademicYear(DateAbstract):
    start_year = models.CharField(max_length=20)
    end_year = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.start_year + " - " + self.end_year

class Semester(DateAbstract):
    number = models.CharField(max_length=20)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.course.name} - Semester {self.number}"

class Enrollment(DateAbstract):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    enrollment_number = models.CharField(max_length=50, unique=True)
    roll_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    total_fee = models.CharField(max_length=20, null=True, blank=True)
    paid_fee = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    #status

    def __str__(self):
        return f"{self.user.email} | {self.course.name} | {self.academic_year.start_year} - {self.academic_year.end_year}"
    

class StudentSemester(DateAbstract):

    PASS = "pass"
    FAIL = "fail"
    PROMOTED = "promoted"
    DETAINED = "detained"
    
    RESULT_STATUS_CHOICES = (
        (PASS, "Pass"),
        (FAIL, "Fail"),
        (PROMOTED, "Promoted"),
        (DETAINED, "Detained"),
    )
    
    ENROLLED = "enrolled"
    NOT_STARTED = "not_started"
    CURRENT = "current"
    COMPLETED = "completed"
    FAILED = "failed"
    REPEATED = "repeated"
    
    SEMESTER_STATUS_CHOICES = (
        (ENROLLED, "Enrolled"),
        (NOT_STARTED, "Not Started"),
        (CURRENT, "Current"),
        (COMPLETED, "Completed"),
        (FAILED, "Failed"),
        (REPEATED, "Repeated"),
    )
    
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    attendance_percentage = models.CharField(max_length=10, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    sgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    attempt_number = models.PositiveSmallIntegerField(default=1)
    status = models.CharField(
        max_length=20,
        choices=SEMESTER_STATUS_CHOICES,
        default=CURRENT
    )
    result_status = models.CharField(
        max_length=20,
        choices=RESULT_STATUS_CHOICES,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.enrollment.user.email} - {self.semester.course.name} - Semester {self.semester.number}"


class StudentData(DateAbstract):
    enrollment = models.OneToOneField(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    alternate_mobile_number = models.CharField(max_length=15, null=True, blank=True)
    mother_name = models.CharField(max_length=100, null=True, blank=True)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.enrollment.user.email} - {self.full_name}"

class StudentDocument(DateAbstract):
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="documents"
    )
    document_type = models.CharField(max_length=50)
    document_file = models.FileField(upload_to="student_documents/")
    def __str__(self):
        return f"{self.enrollment.user.email} - {self.document_type}"

class PreviousAcademicRecord(DateAbstract):
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="academic_records"
    )
    institution_name = models.CharField(max_length=100)
    university = models.CharField(max_length=20, null=True, blank=True)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    course = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"{self.enrollment.user.email}"
    

class Subject(models.Model):
    semester = models.ForeignKey(
        Semester,
        on_delete=models.CASCADE,
        related_name="subjects"
    )
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    credits = models.IntegerField()


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20)

class SubjectTeacher(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)

class ClassSession(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()