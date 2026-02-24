from erp.models import Course, Enrollment, AcademicYear, StudentSemester, StudentData, StudentDocument, PreviousAcademicRecord
from auth_app.models import User
from erp.utils import generate_enrollment_number
from django.db import IntegrityError, transaction

class CourseEnrollmentHandler:

    @classmethod
    def enroll_student(cls, request):
        try:
            user_id = request.user.user_id
            print("user_id:", user_id)
            course_id = request.data.get("course_id")
            academic_year_id = 1 #request.data.get("academic_year_id")
            full_name = request.data.get("full_name")
            date_of_birth = request.data.get("date_of_birth")
            print("date_of_birth:", date_of_birth)
            gender = request.data.get("gender")
            address = request.data.get("address")
            institution_name = request.data.get("institution_name")
            university = request.data.get("university")
            course_name = request.data.get("course")
            cgpa = request.data.get("cgpa")
            alternate_mobile_number = request.data.get("alternate_mobile_number")
            mobile_number = request.data.get("mobile_number")
            mother_name = request.data.get("mother_name")
            father_name = request.data.get("father_name")


            if not user_id:
                return {"error": "User ID is required"}

            if not course_id:
                return {"error": "Course ID is required"}

            if not academic_year_id:
                return {"error": "Academic Year ID is required"}
            
            try:
                user = User.objects.get(user_id=user_id, role=User.STUDENT)
                print("user:", user)
            except User.DoesNotExist:
                return {"error": "Valid student not found"}

            try:
                course = Course.objects.get(id=course_id, is_active=True)
            except Course.DoesNotExist:
                return {"error": "Course not found"}

            try:
                academic_year = AcademicYear.objects.get(id=academic_year_id, is_active=True)
            except AcademicYear.DoesNotExist:
                return {"error": "Academic year not found"}

            if Enrollment.objects.filter(
                user=user,
                course=course,
                # status="ACTIVE"
            ).exists():
                return {"error": "Student already enrolled in this course"}
            
            with transaction.atomic():
                enrollment_number = generate_enrollment_number(course, academic_year)

                enrollment = Enrollment.objects.create(
                    user=user,
                    course=course,
                    academic_year=academic_year,
                    enrollment_number=enrollment_number,
                    # status="ACTIVE"
                )

                enrollment_id = enrollment.id
                semester = StudentSemester.objects.create(
                    enrollment=enrollment,
                    status=StudentSemester.ENROLLED,
                    semester=course.semester_set.filter(is_active=True).first() )
                
                student_data = StudentData.objects.create(
                    enrollment=enrollment,
                    full_name=full_name,
                    date_of_birth=date_of_birth,
                    gender=gender,
                    address=address,
                    mobile_number=mobile_number,
                    alternate_mobile_number=alternate_mobile_number,
                    mother_name=mother_name,
                    father_name=father_name
                )

                par = PreviousAcademicRecord.objects.create(
                    enrollment=enrollment,
                    institution_name=institution_name,
                    university=university,
                    course=course_name,
                    cgpa=cgpa
                )

            return {
                "message": "Enrollment successful",
                "student_email": user.email,
                "enrollment_number": enrollment.enrollment_number,
                "course": course.name,
                "academic_year": f"{academic_year.start_year}-{academic_year.end_year}",
            }

        except IntegrityError:
            return {"error": "Enrollment number conflict. Please try again"}

        except Exception as e:
            return {"error": "Something went wrong", "details": str(e)}

    @classmethod
    def list_courses(cls, request):
        courses = Course.objects.filter(is_active=True).values(
            "id",
            "name",
            "description",
            "total_years",
            "total_semesters",
            "total_credits"
        )
        return {"courses": list(courses)}
    
    @classmethod
    def list_academic_years(cls, request):
        years = AcademicYear.objects.filter(is_active=True).values(
            "id",
            "start_year",
            "end_year"
        )
        return {"academic_years": list(years)}
    

    @classmethod
    def get_enrollments(cls, request):
        user_id = request.query_params.get("user_id")
        enrollment_number = request.query_params.get("enrollment_number")
    
        enrollments = (
            Enrollment.objects
            .select_related("course", "academic_year")
            .prefetch_related("profile", "academic_records")
        )
    
        if user_id:
            enrollments = enrollments.filter(
                user__user_id=user_id,
                user__role=User.STUDENT
            )
    
        if enrollment_number:
            enrollments = enrollments.filter(
                enrollment_number=enrollment_number
            )
    
        result = []
    
        for enrollment in enrollments:
            profile = enrollment.profile 
    
            result.append({
                "enrollment_number": enrollment.enrollment_number,
                "course": enrollment.course.name,
                "academic_year": f"{enrollment.academic_year.start_year}-{enrollment.academic_year.end_year}",
                "profile": {
                    "full_name": profile.full_name if profile else None,
                    "date_of_birth": profile.date_of_birth if profile else None,
                    "gender": profile.gender if profile else None,
                    "mobile_number": profile.mobile_number if profile else None,
                    "alternate_mobile_number": profile.alternate_mobile_number if profile else None,
                    "mother_name": profile.mother_name if profile else None,
                    "father_name": profile.father_name if profile else None,
                    "address": profile.address if profile else None,
                },
                "academic_records": [
                    {
                        "institution_name": record.institution_name,
                        "university": record.university,
                        "course": record.course,
                        "cgpa": record.cgpa
                    }
                    for record in enrollment.academic_records.all()
                ]
            })
    
        return {"enrollments": result}