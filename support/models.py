from django.db import models
from django.contrib.auth import get_user_model
from .choices import SUPPORT_REQUEST_STATUSES

User = get_user_model()


class SupportRequestModel(models.Model):
    """ Stores customer support request data
    """
    
    class Meta:
        verbose_name = "Support request"
        verbose_name_plural = "Support requests"
        ordering = ['-created_at']
        

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="support_requests",
        related_query_name="support_request",
        null=True,
        blank=True,  
    )
    
    email = models.EmailField(null=True)
    
    subject = models.CharField(max_length=60, default='')
    request = models.TextField(default='', blank=True)
    
    status = models.CharField(max_length=1, choices=SUPPORT_REQUEST_STATUSES, default="P")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self) -> str:
        return f"Support request from {self.user} {self.get_status_display()}"