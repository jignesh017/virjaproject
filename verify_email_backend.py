import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vproject.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def verify_backend():
    print(f"Current EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print("Attempting to send test email using standard send_mail...")
    
    try:
        send_mail(
            'Test Email from Database Backend',
            'This is a test email to verify that the custom DatabaseEmailBackend is working correctly.',
            'test@example.com',
            ['bhutjaydip1554@gmail.com'], # Sending to the user's email
            fail_silently=False,
        )
        print("SUCCESS: Email sent successfully!")
    except Exception as e:
        print(f"FAILURE: Could not send email.")
        print(f"Error Details: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify_backend()
