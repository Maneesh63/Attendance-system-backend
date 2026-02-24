import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
import jwt
from django.conf import settings

def generate_user_qr_token(user):
    payload = {
        "user_id": str(user.user_id),
        "type": "user_qr"
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

def generate_user_qr_image(token):
    qr = qrcode.make(token)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return ContentFile(buffer.getvalue(), name="user_qr.png")