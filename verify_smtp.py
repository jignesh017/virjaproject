import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vproject.settings')
django.setup()

from core.models import SMTPSettings
from django.core.mail import get_connection, EmailMessage

def verify_smtp():
    print("--- Starting SMTP Verification ---")
    smtp = SMTPSettings.objects.first()
    if not smtp:
        print("Error: No SMTP Settings found in database.")
        return

    print(f"Host: {smtp.email_host}")
    print(f"Port: {smtp.email_port}")
    print(f"User: {smtp.email_host_user}")
    print(f"TLS: {smtp.email_use_tls}")
    print(f"SSL: {smtp.email_use_ssl}")
    print("----------------------------------")

    try:
        connection = get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host=smtp.email_host,
            port=smtp.email_port,
            username=smtp.email_host_user,
            password=smtp.email_host_password,
            use_tls=smtp.email_use_tls,
            use_ssl=smtp.email_use_ssl,
            timeout=10
        )
        
        print("Attempting to open connection...")
        connection.open()
        print("SUCCESS: Connection opened successfully!")
        connection.close()
        print("Connection closed.")
        
    except Exception as e:
        print(f"FAILURE: Could not connect to SMTP server.")
        print(f"Error Details: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify_smtp()
