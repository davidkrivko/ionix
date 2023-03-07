from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from properties.models import ZipCodeModel
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    username = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
  
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username}"


class ProfileAbstractModel(models.Model):
    class Meta:
        abstract = True

    first_name = models.CharField(max_length=60, default='', blank=True)
    logo = models.ImageField(null=True, blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OwnerProfileModel(ProfileAbstractModel):

    class Meta:
        verbose_name = "Owner"
        verbose_name_plural = "Owners"
        ordering = ['-created_at']

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="owner",
    )
    phone_number = PhoneNumberField(default='', blank=True)
    nickname = models.CharField(max_length=60, default='', blank=True)
    is_landlord = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user}"


class ProviderProfileModel(ProfileAbstractModel):

    class Meta:
        verbose_name = "Services provider"
        verbose_name_plural = "Services providers"
        ordering = ['-created_at']

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="provider",
    )

    zip = models.ForeignKey(
        ZipCodeModel,
        on_delete=models.SET_NULL,
        null=True,
        help_text="Property ZIP code"
    )
    company = models.CharField(max_length=120, default='', help_text="Company name")
    phone_number = PhoneNumberField()

    def __str__(self) -> str:
        return f"{self.company}"


class StaffProfileModel(ProfileAbstractModel):
    class Meta:
        verbose_name = "Staff user"
        verbose_name_plural = "Staff users"
        ordering = ['-created_at']

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="staffuser",
    )

    def __str__(self) -> str:
        return f"Employee {self.first_name}"


class TenantProfileModel(ProfileAbstractModel):

    class Meta:
        verbose_name = "Tenant profile"
        verbose_name_plural = "Tenant profiles"
        ordering = ['-created_at']

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="tenant",
        null=True,
    )

    owner = models.ForeignKey(
        OwnerProfileModel,
        on_delete=models.CASCADE,
        related_name="tenants",
        related_query_name="tenant",
        null=True,
    )

    rooms = models.ManyToManyField(
        'properties.RoomModel',
        related_name="tenants",
        related_query_name="tenant",
        blank=True,
        help_text="Assigned rooms"
    )

    is_guest = models.BooleanField(default=False)
    access_link = models.CharField(max_length=120, default='', blank=True)
    password_reset_needed = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"Tenant: {self.first_name}"
