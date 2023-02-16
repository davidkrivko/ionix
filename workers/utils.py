from django.core.mail import send_mail
from django_q.tasks import async_task
from django.conf import settings

DEFAULT_ADMIN_EMAIL = settings.DEFAULT_ADMIN_EMAIL



def send_email(subject, plain_text, recipient):
    """
    Core django sendmail wrapper with async implementation
    """
    #add template rendering
    html = None
    send_mail(subject=subject, message=plain_text, html_message=html, from_email = None, recipient_list=[DEFAULT_ADMIN_EMAIL])
    # async_task('django.core.mail.send_mail', subject=subject, message=plain_text, html_message=html, from_email = None, recipient_list=[recipient])