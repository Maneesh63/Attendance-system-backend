
from urllib import request
from attendance.utils import generate_user_qr_token, generate_user_qr_image
from auth_app.models import UserQR
from attendance.models import AttendanceRecord
from django.utils import timezone
from auth_app.jwt_handler import decode_jwt
from erp.utils import S3Handler
import traceback
from io import BytesIO

baseurl = "http://127.0.0.1:8000"

class AttendanceHandler:

    @classmethod
    def create_user_qr(cls, request):
        user = request.user

        if UserQR.objects.filter(user=user, is_active=True).exists():
            return {"error": "QR Code already exists"}

        try:
            token = generate_user_qr_token(user)
            print("token:", token)
            image = generate_user_qr_image(token)
            user_qr = UserQR.objects.create(
                user=user,
                qr_token=token,
                qr_image=image
            )
            
            image_url = baseurl + user_qr.qr_image.url
            print("Generated QR code image URL 1st:", image_url)
            try:
                 
                image.seek(0)   
                image_bytes = image.read() 
                file_name = f"qr_images/{user_qr.id}.png"
                print("Uploading file to S3 with name:", file_name)
                file_options = {"content-type": "image/png"}
                public_url = S3Handler.upload_file_to_s3(
                    file_bytes=image_bytes,
                    file_path=file_name,
                    file_options=file_options
                )
                return {
                        "message": "QR code created successfully",
                        "qr_token": user_qr.qr_token,
                        "qr_image_url": image_url,
                        "sb__qr_image_url": public_url
                    }

            except Exception as e:
                traceback.print_exc()
                return {"error": "Failed to generate QR code image."}
                
        except Exception as e:
            return {"error": "Failed to create QR code"}

    @classmethod
    def mark_attendance(cls, request):
        
        token = request.data.get("qr_token")
        if not token:
            return {"error": "QR token is required"}
        
        payload = decode_jwt(token)
        print("payload:", payload)

        if not payload or payload.get("type") != "user_qr":
            return {"error": "Invalid or tampered QR"}
        
        user_id = payload.get("user_id")
        user = request.user
        if str(request.user.user_id) != user_id:
               print("User ID mismatch: token user_id:", type(user_id), "request user_id:", type(request.user.user_id))
               return {"error": "QR code Mismatch"} 
        try:
            user_qr = UserQR.objects.get(user__user_id=user_id, qr_token=token, is_active=True)
        except UserQR.DoesNotExist:
            return {"error": "QR revoked or not found"}
        
        today = timezone.localdate()
        print("today:", today)
        user = user_qr.user
        check_in = timezone.now()
        print("check_in:", check_in)
        status = "present"
        
        record, created = AttendanceRecord.objects.get_or_create(
            user=user,
            date=today,
            defaults={
                "check_in_time": check_in,
                "check_out_time": None,
                "status": status
            }
        )

        if not created:
            return {
                "message": "Attendance already marked",
                "date": str(today),
                "check_in_time": record.check_in_time.isoformat(),
                "status": record.status
            }
        
        return {
            "message": "Attendance marked successfully",
            "date": str(today),
            "check_in_time": record.check_in_time.isoformat(),
            "status": record.status
        } 
        