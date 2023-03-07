from django.db.models.signals import post_save, pre_save
from django.utils import timezone
import logging
from .models import TenantProfileModel
from django_q.tasks import async_task

now = timezone.now


def trigger_first_password_email(sender, instance, created, **kwargs):
    """
    If child user / tenant was created, schedule and email with
    access link to access profile and change password
    """
    if created and instance.is_guest is False:
        # if instance.is_guest == False:
        async_task("users.utils.send_tenant_password_reset_link", instance.pk)
        async_task('workers.tasks.apartment_occupied_now', instance.pk)


post_save.connect(trigger_first_password_email, sender=TenantProfileModel)
