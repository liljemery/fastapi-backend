"""
Email utility functions
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional

from config import settings


def send_email(
    to_emails: List[str],
    subject: str,
    body: str,
    html_body: Optional[str] = None
) -> bool:
    """
    Send email
    
    Args:
        to_emails: List of recipient emails
        subject: Email subject
        body: Plain text body
        html_body: HTML body (optional)
        
    Returns:
        True if sent successfully
    """
    # TODO: Implement email sending logic
    pass

