from django.core.mail import send_mail
from users.models import TenantProfileModel
import logging
from users.owners.api import CURRENT_SITE
from users.tokens import password_reset_tokenizer
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings

from django.urls import reverse

User = get_user_model()
CURRENT_SITE = settings.CURRENT_SITE



def send_tenant_password_reset_link(tenant_id: int, email: str = None):
    """Send insurance quote details once
    request was signed with BankID (signal)
    """
    try:
        tenant = TenantProfileModel.objects.get(pk=tenant_id)
    except Exception as e:
        tenant = None
        logging.warning("Tenant profile not found")
        return e

    if email is None:
        email = tenant.user.username
        
    url = tenant.access_link
    subject = "Boiler management panel"
    content = f"Hello {tenant.first_name}, You've been invited to boiler management control panel. Please, follow the link to access your new account and set your first password: {url}"

    send_mail(
        subject,
        content,
        None,
        [email],
        fail_silently=False,
    )


def update_tenant_password_reset_success(tenant_id: int):
    """"Update tenant profile to store stae about password
    reset event
    """
    try:
        tenant = TenantProfileModel.objects.get(pk=tenant_id)
    except Exception as e:
        tenant = None
        logging.warning("Tenant profile not found")
        return e

    tenant.password_reset_needed = False
    tenant.save()

    return "OK"



def send_password_reset_link(user_pk: int):

    user = User.objects.get(pk = user_pk)

    token = password_reset_tokenizer.make_token(user)
    user_id = urlsafe_base64_encode(force_bytes(user_pk))
    url = CURRENT_SITE + reverse('reset-validate', kwargs={'user_id': user_id, 'token': token})
    email = user.username
    subject = "Boiler management panel"
    content = f"Hello, we've just received a password reset request for your account at turnonheat.com. Please follow the link to set your new password : {url} "

    send_mail(
        subject,
        content,
        None,
        [email],
        fail_silently=False,
    )