import requests, random
from typing import Literal, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.services.communication.models.otp import OTPModel

class SMSUtils:
    @staticmethod
    def send_sms(
            phone_number: str,
            message: str,
            provider: Literal["fast2sms", "smshorizon", "textlocal", "exotel"],
            api_key: str = None,
            sender_id: Optional[str] = None,
            sid: Optional[str] = None,
            token: Optional[str] = None,
    ) -> dict:
        """
        Sends an SMS using the specified provider.

        :param phone_number: Recipient's phone number (Indian number without +91)
        :param message: SMS content
        :param provider: SMS provider name ("fast2sms", "smshorizon", "textlocal", "exotel")
        :param api_key: API key for authentication
        :param sender_id: Sender ID (Required for some providers)
        :param sid: SID (Only for Exotel)
        :param token: Auth Token (Only for Exotel)
        :return: Response JSON or text
        """

        if provider == "fast2sms":
            url = "https://www.fast2sms.com/dev/bulkV2"
            payload = {
                "message": message,
                "language": "english",
                "route": "q",
                "numbers": phone_number,
            }
            headers = {
                "authorization": "td7Ywhi2FgMokNjxRA0IPzKVZC3fen4Uv8SuL9brEXslQmq1WBSLJqpsWnD4eNvGclI0UyFXgwu98zQh",
                "cache-control": "no-cache"
            }

            response = requests.post(url, data=payload, headers=headers)
            print(response.json())
            return response.json()

        elif provider == "smshorizon":
            url = f"https://www.smshorizon.in/api/sendsms.php?user=your_username&apikey={api_key}&mobile={phone_number}&message={message}&senderid={sender_id}&type=txt"
            response = requests.get(url)
            return response.text

        elif provider == "textlocal":
            url = "https://api.textlocal.in/send/"
            payload = {
                "apikey": api_key,
                "numbers": phone_number,
                "message": message,
                "sender": sender_id or "TXTLCL",
            }
            response = requests.post(url, data=payload)
            return response.json()

        elif provider == "exotel":
            if not (sid and token):
                raise ValueError("Exotel requires 'sid' and 'token'.")
            url = f"https://api.exotel.com/v1/Accounts/{sid}/Sms/send"
            payload = {
                "From": sender_id,
                "To": phone_number,
                "Body": message,
            }
            response = requests.post(url, data=payload, auth=(sid, token))
            return response.json()

        else:
            raise ValueError("Invalid provider. Choose from 'fast2sms', 'smshorizon', 'textlocal', 'exotel'.")

    def generate_otp(self, db: Session, phone_number: str) -> str:
        """
        Generates a 6-digit OTP, stores it in the database, and replaces any existing OTP.
        """
        otp = str(random.randint(100000, 999999))  # Generate OTP

        # Delete old OTP if exists
        db.query(OTPModel).filter(OTPModel.phone_number == phone_number).delete()

        # Insert new OTP
        otp_entry = OTPModel(phone_number=phone_number, otp=otp)
        db.add(otp_entry)
        db.commit()

        self.send_sms(phone_number=phone_number,message=f"Your otp is {otp}", provider="fast2sms")

        return otp

    @staticmethod
    def verify_otp(db: Session, phone_number: str, otp: str) -> bool:
        """
        Verifies OTP from the database.
        """
        otp_entry = db.query(OTPModel).filter(
            OTPModel.phone_number == phone_number,
            OTPModel.otp == otp,
            OTPModel.created_at >= datetime.utcnow() - timedelta(minutes=5)  # Expiry check
        ).first()

        if otp_entry:
            db.delete(otp_entry)
            db.commit()
            return True
        return False

