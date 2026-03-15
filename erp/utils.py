from erp.models import Enrollment
from rest_framework.exceptions import ValidationError
from root.settings import SUPABASE_S3_STORAGE


def generate_enrollment_number(course, academic_year):
    year = academic_year.start_year
    course_code = course.name[:3].upper()

    count = Enrollment.objects.filter(
        course=course,
        academic_year=academic_year
    ).count() + 1
    
    return f"{year}{course_code}{str(count).zfill(4)}"

class S3Handler:
    
    @classmethod
    def upload_file_to_s3(cls, bucket="qr_image", file_bytes=None, file_path=None, file_options=None, delete=False):
        try:
           
           upload_to_s3 =  SUPABASE_S3_STORAGE.storage.from_(bucket).upload(file_path, file_bytes, file_options)

           public_url = SUPABASE_S3_STORAGE.storage.from_(bucket).get_public_url(file_path)
           
        #    if delete and delete == True:
        #         delete_file = supabase.storage.from_("ecomx").remove([file_path])
        #         if delete_file:
        #             logger.info(f"File {file_path} deleted successfully.")


           return public_url
        except Exception as e:
            if hasattr(e, 'response'):
               print("Status Code:", e.response.status_code)
               print("Raw Response Text:", e.response.text)

            import traceback; traceback.print_exc()
            raise ValidationError({
                "detail": "Failed to upload file.",
                "error": str(e)
            })
               
        