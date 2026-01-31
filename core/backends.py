from django.core.mail.backends.smtp import EmailBackend
from core.models import SMTPSettings
from django.conf import settings

class DatabaseEmailBackend(EmailBackend):
    def __init__(self, host=None, port=None, username=None, password=None,
                 use_tls=None, fail_silently=False, use_ssl=None, timeout=None,
                 ssl_keyfile=None, ssl_certfile=None,
                 **kwargs):
        
        # Load settings from database
        try:
            smtp_settings = SMTPSettings.objects.first()
        except:
            # Handle case where DB might not be ready (e.g. during migrations)
            smtp_settings = None

        if smtp_settings:
            host = smtp_settings.email_host
            port = smtp_settings.email_port
            username = smtp_settings.email_host_user
            password = smtp_settings.email_host_password
            use_tls = smtp_settings.email_use_tls
            use_ssl = smtp_settings.email_use_ssl
            # You might also want to set default_from_email globally if possible, 
            # but EmailBackend doesn't handle that directly. 
            # It's usually handled by the EmailMessage constructor or settings.DEFAULT_FROM_EMAIL.

        super().__init__(host=host, port=port, username=username, password=password,
                         use_tls=use_tls, fail_silently=fail_silently, use_ssl=use_ssl,
                         timeout=timeout, ssl_keyfile=ssl_keyfile, ssl_certfile=ssl_certfile,
                         **kwargs)
