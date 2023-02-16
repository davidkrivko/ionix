from tabnanny import verbose
from django.db import models
from devices.models import (
    AnalogueThermostatModel, 
    SmartThermostatModel, 
    BoilerModel, 
    SimpleSwitchModel,
)
from .choices import ZONE_TYPES, ROOM_TYPES

class ZipCodeModel(models.Model):

    class Meta:
        verbose_name = "ZIP code"
        verbose_name_plural = "ZIP codes"
        ordering = ['-created_at']

    zip_code = models.CharField(max_length=12, default='')

    lat_coord = models.DecimalField(
        decimal_places=4,
        max_digits=8,
        null=True, 
        blank=True, 
        help_text="Approx. latitude coordinate of the property: 39.7456"
        )
    lon_coord = models.DecimalField(
        decimal_places=4,
        max_digits=8,
        null=True,
        blank=True, 
        help_text="Approx. longitude coordinate of the property: -97.0892"
        )

    todays_temp = models.IntegerField(
        null=True,
        blank=True,
        help_text="Last temperature from weather.gov API in °F"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return f"{self.zip_code} {self.updated_at}"

class ZoneAbstractModel(models.Model):

    class Meta:
        abstract = True

    name = models.CharField(max_length=120, default='')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class ZoneModel(ZoneAbstractModel):
    """Zone model describes heating loop only
    """
    class Meta:
        verbose_name = "Heating zone"
        verbose_name_plural = "Heating zones"
        ordering = ['-created_at']

    controller = models.ForeignKey(
        'devices.IoniqControllerModel',
        on_delete=models.SET_NULL,
        null=True,
        related_name="zones",
        related_query_name="zone",
        help_text="Related controller",
        blank=True,
    )
    type = models.CharField(
        max_length=3,
        choices=ZONE_TYPES,
        default='',
        blank=True,
        help_text="Connection type which was set for this zone",
    )

    logo = models.ImageField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name} {self.controller} "



class PropertyAbstractModel(models.Model):
    
    class Meta:
        abstract = True

    name = models.CharField(max_length=120, default='')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class BuildingModel(PropertyAbstractModel):

    class Meta:
        verbose_name = "Building"
        verbose_name_plural = "Buildings"
        ordering = ['-created_at']


    owner = models.ForeignKey(
        'users.OwnerProfileModel',
        on_delete=models.CASCADE,
        related_name="buildings",
        related_query_name="building",
        help_text="Property owner",
    )

    address = models.CharField(max_length=120, default='', blank=True)

    floors_number = models.SmallIntegerField(null=True, blank=True)
    apartments_number = models.SmallIntegerField(null=True, blank=True)

    zip_code = models.ForeignKey(
        ZipCodeModel,
        on_delete=models.SET_NULL,
        related_name="buildings",
        related_query_name="building",
        null=True,
        help_text="Property zip code"
    )

    boiler = models.OneToOneField(
        BoilerModel,
        on_delete=models.SET_NULL,
        related_name="buildings",
        related_query_name="building",
        null=True,
        blank=True,
        help_text="Installed boiler",
    )

    provider = models.ForeignKey(
        'users.ProviderProfileModel',
        on_delete=models.SET_NULL,
        related_name="buildings",
        related_query_name="building",
        null=True,
        blank=True,
        help_text="Assigned services provider"
    )


    def __str__(self) -> str:
        return f"{self.name} {self.owner}"


class ApartmentModel(PropertyAbstractModel):

    class Meta:
        verbose_name = "Apartment"
        verbose_name_plural = "Apartments"
        ordering = ['-created_at']

    
    building = models.ForeignKey(
        BuildingModel,
        on_delete=models.CASCADE,
        related_name="apartments",
        related_query_name="apartment",
        null=True,
        help_text="The building this apartment is a part of"
    )

    boiler = models.ForeignKey(
        BoilerModel,
        on_delete=models.SET_NULL,
        related_name="apartments",
        related_query_name="apartment",
        null=True,
        blank=True,
        help_text="Installed boiler",
    )

    rooms_number = models.SmallIntegerField(null=True, blank=True)
    leaseholder = models.CharField(max_length=120, default='', blank=True)
    is_vacant = models.BooleanField(default=False)
    is_alert = models.BooleanField(
        default=False, 
        help_text="Checked automatically if was flagged by sysem checks. Details in the related alert model."
        )
    
    tlimits_is_on = models.BooleanField(default=False, help_text="If enabled, tenants won't be able to set their thermostat outside of landlord range")
    min_temp = models.SmallIntegerField(null=True, blank=True)
    max_temp = models.SmallIntegerField(null=True, blank=True)
    
    def __str__(self) -> str:
        return f"{self.name} {self.building}"


class RoomModel(PropertyAbstractModel):

    class Meta:
        verbose_name = "Rooom"
        verbose_name_plural = "Rooms"
        ordering = ['-created_at']
    

    size = models.SmallIntegerField(
        null=True,
        blank=True,
        help_text="Room size in sq ft"
    )

    heat_source = models.SmallIntegerField(
        null=True,
        blank=True,
        help_text="- Heat source BTU/H"
    )
    
    apartment = models.ForeignKey(
        ApartmentModel,
        on_delete=models.CASCADE,
        related_name="rooms",
        related_query_name="room",
        null=True,
        help_text="The apartment this room is a part of"
    )

    room_type = models.CharField(
        max_length=2,
        choices=ROOM_TYPES,
        default='',
    )

    thermostat = models.ForeignKey(
        SmartThermostatModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Dedicated smart thermostat"
    )

    heat_switch = models.ForeignKey(
        SimpleSwitchModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Related heat-switch if conneceted",
    )

    analogue_thermostat = models.ForeignKey(
        AnalogueThermostatModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Related analogue thermostat if conneceted",
    )

    def __str__(self) -> str:
        return f"{self.name} {self.apartment} type: {self.get_room_type_display()}"


class ApartmentAlertDetailsModel(models.Model):

    class Meta:
        verbose_name = "Apartment alerts"
        verbose_name_plural = "Apartment alert"
        ordering = ['-created_at']

    apartment = models.ForeignKey(
        ApartmentModel,
        on_delete=models.CASCADE,
        related_name="alerts",
        related_query_name="alert"
    )
    details = models.TextField(default='')    

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return f"{self.created_at.date()} {self.apartment}"


class WeatherRecordModel(models.Model):
    """
    Stores weather.gov temp data
    """

    class Meta:
        verbose_name = "Temperature record"
        verbose_name_plural = "Temperature records"
        ordering = ['-created_at']

    zip_code = models.ForeignKey(
        ZipCodeModel,
        on_delete=models.CASCADE,
        related_name="temperatures",
        related_query_name="temperature",
        null=True,
    )

    temp_f = models.IntegerField(
        null=True,
        blank=True,
        help_text="Temp value from weather.gov API in °F"
    )

    temp_c = models.IntegerField(
        null=True,
        blank=True,
        help_text="Temp value from weather.gov API in °C"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Temp record for {self.zip_code} timestamp: {self.created_at}"