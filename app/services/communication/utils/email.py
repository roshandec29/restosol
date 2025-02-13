import aiosmtplib
from email.message import EmailMessage
from app.config import config


async def send_email(recipient: str, subject: str, message: str) -> bool:
    try:
        msg = EmailMessage()
        msg["From"] = config.EMAIL_USERNAME
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.set_content(message)

        print(config.EMAIL_PASSWORD)

        # Connect to SMTP server and send email
        await aiosmtplib.send(
            msg,
            hostname=config.EMAIL_HOST,
            port=config.EMAIL_PORT,
            username=config.EMAIL_USERNAME,
            password=config.EMAIL_PASSWORD,
            use_tls=False,
            start_tls=True,  # Important for security
        )

        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False


def registration_email():
    email_body = """\
    Hey,

    Thank you for joining RestoSol! We’re excited to have you on board.

    Your account has been successfully created, and you can now explore all the features we offer. If you have any questions or need assistance, feel free to reach out to our support team.

    Next Steps:
    ✅ Log in to your account: [Login URL]
    ✅ Explore our features: [Features URL]
    ✅ Need help? Contact us at [Support Email]

    We look forward to providing you with a great experience!

    Best regards,  
    RestoSol
    """
    return email_body
