from django.core.mail import get_connection, send_mail
from django.core.mail.message import EmailMessage, EmailMultiAlternatives
from core.models import SMTPSettings
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def get_custom_email_connection():
    """
    Returns a configured email backend connection using database settings.
    """
    smtp = SMTPSettings.objects.first()
    if not smtp or not smtp.email_host_user:
        return None
        
    try:
        connection = get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host=smtp.email_host,
            port=smtp.email_port,
            username=smtp.email_host_user,
            password=smtp.email_host_password,
            use_tls=smtp.email_use_tls,
            use_ssl=smtp.email_use_ssl,
        )
        return connection
    except Exception as e:
        logger.error(f"Failed to create email connection: {e}")
        return None

def send_custom_email(subject, message, recipient_list, from_email=None, html_message=None, attachments=None):
    """
    Sends an email using the custom SMTP settings from the database.
    If no settings are found, falls back to default Django settings.
    """
    smtp = SMTPSettings.objects.first()
    
    # Check if we have dynamic settings
    if smtp and smtp.email_host_user:
        connection = get_custom_email_connection()
        if connection:
            if not from_email:
                from_email = smtp.default_from_email
            
            try:
                # Use EmailMultiAlternatives for both text and HTML
                email = EmailMultiAlternatives(
                    subject,
                    message,
                    from_email,
                    recipient_list,
                    connection=connection
                )
                if html_message:
                    email.attach_alternative(html_message, "text/html")
                
                if attachments:
                    for attachment in attachments:
                        # attachment should be tuple (filename, content, mimetype)
                        email.attach(*attachment)
                
                email.send(fail_silently=False)
                return True
            except Exception as e:
                logger.error(f"Failed to send custom email: {e}")
                print(f"DEBUG: Failed to send custom email: {e}")
    
    # Fallback to default Django send_mail/EmailMessage
    try:
        if attachments:
            email = EmailMultiAlternatives(
                subject,
                message,
                from_email or settings.DEFAULT_FROM_EMAIL,
                recipient_list
            )
            if html_message:
                email.attach_alternative(html_message, "text/html")
            for attachment in attachments:
                email.attach(*attachment)
            email.send(fail_silently=False)
        else:
            send_mail(subject, message, from_email or settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=False, html_message=html_message)
        return True
    except Exception as e:
        logger.error(f"Failed to send fallback email: {e}")
        print(f"DEBUG: Failed to send fallback email: {e}")
        return False
    
    # Fallback to default Django send_mail
    try:
        if attachments:
            # send_mail doesn't support attachments easily, use EmailMessage for fallback too
            email = EmailMessage(
                subject,
                html_message or message,
                from_email or settings.DEFAULT_FROM_EMAIL,
                recipient_list
            )
            if html_message:
                email.content_subtype = "html"
            for attachment in attachments:
                email.attach(*attachment)
            email.send(fail_silently=False)
        else:
            send_mail(subject, message, from_email or settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=False, html_message=html_message)
        return True
    except Exception as e:
        logger.error(f"Failed to send fallback email: {e}")
        print(f"DEBUG: Failed to send fallback email: {e}")
        return False
