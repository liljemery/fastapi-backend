import smtplib
import ssl
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from typing import Optional, Dict, List, Tuple, Union
from config import settings

def send_email(
    *,
    to_email: str,
    subject: str,
    html_content: str,
    plain_text: Optional[str] = None,
    from_email: Optional[str] = None,
    attachments: Optional[List[Tuple[str, bytes, str]]] = None,
) -> Dict[str, str]:
    """
    Send an HTML email with optional plain text and file attachments.

    Args:
        to_email:      Recipient's email address.
        subject:       Email subject.
        html_content:  HTML content (complete string).
        plain_text:    Alternative text (optional).
        from_email:    Sender (defaults to settings.EMAIL_USER).
        attachments:   List of tuples (filename, file_bytes, content_type) (optional).

    Returns:
        {"status": "sent"}          if everything goes well
        {"error":  "<message>"}     if any problem occurs
    """
    try:
        # Validate email credentials
        if not settings.EMAIL_USER or not settings.EMAIL_PASSWORD:
            return {"error": "Email credentials not configured"}
        
        # Set default sender
        sender = from_email or settings.EMAIL_USER

        # Create message based on whether we have attachments
        msg: Union[MIMEMultipart, EmailMessage]
        
        if attachments:
            # Create multipart message for attachments
            msg = MIMEMultipart('alternative')
            msg["Subject"] = subject
            msg["From"] = sender
            msg["To"] = to_email

            # Add text content
            if plain_text:
                part1 = MIMEText(plain_text, 'plain')
                msg.attach(part1)

            # Add HTML content
            part2 = MIMEText(html_content, 'html')
            msg.attach(part2)

            # Add file attachments
            for filename, file_bytes, content_type in attachments:
                attachment = MIMEApplication(file_bytes, _subtype=content_type.split('/')[-1])
                attachment.add_header('Content-Disposition', 'attachment', filename=filename)
                msg.attach(attachment)
        else:
            # Simple message without attachments using EmailMessage
            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = sender
            msg["To"] = to_email

            if plain_text:
                msg.set_content(plain_text)
            else:
                # Fallback for non-HTML clients
                msg.set_content("HTML email — open in an HTML-capable viewer.")

            # HTML part
            msg.add_alternative(html_content, subtype="html")

        # Secure connection and sending
        context = ssl._create_unverified_context()
        with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT, context=context) as smtp:
            smtp.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
            smtp.send_message(msg)

        return {"status": "sent"}

    except smtplib.SMTPAuthenticationError:
        return {"error": "SMTP authentication failed. Check credentials or app-password."}
    except smtplib.SMTPException as e:
        return {"error": f"SMTP error: {e}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}


send_email_with_attachment = send_email