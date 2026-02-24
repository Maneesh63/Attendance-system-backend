from erp.models import Enrollment


def generate_enrollment_number(course, academic_year):
    year = academic_year.start_year
    course_code = course.name[:3].upper()

    count = Enrollment.objects.filter(
        course=course,
        academic_year=academic_year
    ).count() + 1
    
    return f"{year}{course_code}{str(count).zfill(4)}"