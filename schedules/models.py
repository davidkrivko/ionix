from django.db import models
from devices.models import (
    BoilerModel,
    SmartThermostatModel,
    SimpleSwitchModel,
    AnalogueThermostatModel,
)
from properties.models import ZoneModel
from .choices import WEEK_DAYS
from users.models import OwnerProfileModel
import pytz


class DeviceScheduleModel(models.Model):

    class Meta:
        verbose_name = "Schedule window"
        verbose_name_plural = "Schedule windows"
        ordering = ['checkpoint']

    week_day = models.SmallIntegerField(choices=WEEK_DAYS, default=1)

    checkpoint = models.DateTimeField(
        help_text="Primary timestamp for scheduled execution"
        )

    def __str__(self) -> str:
        return f"Checkpoint for {self.get_week_day_display()} at {self.checkpoint.astimezone(pytz.timezone('US/Eastern')).time().strftime('%H:%M')}"


class ThermostatSubscriberModel(models.Model):

    class Meta:
        verbose_name = "Thermostat subscriber"
        verbose_name_plural = "Thermostat subscribers"
        ordering = ['-updated_at']

    schedule = models.ForeignKey(
        DeviceScheduleModel,
        on_delete=models.CASCADE,
        related_name="subscribers",
        related_query_name="subscriber",
    )

    thermostat = models.ForeignKey(
        SmartThermostatModel,
        on_delete=models.CASCADE,
        help_text="Smart thermostat which should be updated",
    )
    
    owner = models.ForeignKey(
        OwnerProfileModel,
        on_delete=models.CASCADE,
        related_name="schedules",
        related_query_name="schedule",
        null=True,
        blank=True,
    )

    setpoint = models.SmallIntegerField(null=True, help_text="Value to override smart thermostat setpoint field")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.schedule} {self.thermostat}"


class HeatSwitchSubscriberModel(models.Model):

    class Meta:
        verbose_name = "Heatswitch subscriber"
        verbose_name_plural = "Heatswitch subscribers"
        ordering = ['-updated_at']

    schedule = models.ForeignKey(
        DeviceScheduleModel,
        on_delete=models.CASCADE,
        related_name="heat_switches",
        related_query_name="heat_switch",
    )

    switch = models.ForeignKey(
        SimpleSwitchModel,
        on_delete=models.CASCADE,
        help_text="Heat switch which should be updated",
    )
    
    owner = models.ForeignKey(
        OwnerProfileModel,
        on_delete=models.CASCADE,
        related_name="heatswitch_schedules",
        related_query_name="heatswitch_schedules",
        null=True,
        blank=True,
    )

    status = models.BooleanField(default=True, help_text="Heat switch status to set")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.schedule} {self.switch}"


class AnalogueThermostatSubscriberModel(models.Model):

    class Meta:
        verbose_name = "Analogue subscriber"
        verbose_name_plural = "Analogue subscribers"
        ordering = ['-updated_at']

    schedule = models.ForeignKey(
        DeviceScheduleModel,
        on_delete=models.CASCADE,
        related_name="analogue_switches",
        related_query_name="analogue_switch",
    )

    analogue_thermostat = models.ForeignKey(
        AnalogueThermostatModel,
        on_delete=models.CASCADE,
        help_text="Analogue thermostat which should be updated",
    )
    
    owner = models.ForeignKey(
        OwnerProfileModel,
        on_delete=models.CASCADE,
        related_name="analogue_schedules",
        related_query_name="analogue_schedules",
        null=True,
        blank=True,
    )

    status = models.BooleanField(default=True, help_text="Analogue thermostat status to set")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.schedule} {self.analogue_thermostat}"


class ZoneSubscriberModel(models.Model):
    class Meta:
        verbose_name = "Heating zone subscriber"
        verbose_name_plural = "Heating zones subscribers"
        ordering = ['-updated_at']

    schedule = models.ForeignKey(
        DeviceScheduleModel,
        on_delete=models.CASCADE,
        related_name="zones",
        related_query_name="zone",
    )

    heating_zone = models.ForeignKey(
        ZoneModel,
        on_delete=models.CASCADE,
        help_text="Smart thermostat which should be updated",
    )

    owner = models.ForeignKey(
        OwnerProfileModel,
        on_delete=models.CASCADE,
        related_name="zone_schedules",
        related_query_name="zone_schedule",
        null=True,
        blank=True,
    )

    setpoint = models.SmallIntegerField(null=True, help_text="Value to override smart thermostat setpoint field")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.schedule} {self.heating_zone}"


# class LandlordOffHoursScheduleModel(models.Model):
#     """
#     Stores off-hours schedule settings for all
#     boiler-controller-zones devices
#     """

#     class Meta:
#         verbose_name = "Landlord off-hours schedule"
#         verbose_name_plural = "Landlord off-hours schedules"
#         ordering = ['owner']

#     start_checkpoint = models.TimeField(
#         help_text="Offhours start Fieldstamp"
#         )
    
#     end_checkpoint = models.TimeField(
#         help_text="Offhours end timestamp"
#         )
    
#     setpoint = models.SmallIntegerField(null=True, help_text="Value to override smart thermostat setpoint field")

#     owner = models.ForeignKey(
#         OwnerProfileModel,
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#     )

#     boiler = models.ForeignKey(
#         BoilerModel,
#         on_delete=models.CASCADE,
#         related_name="offhours_schedule",
#         related_query_name="offhours_schedules",
#     )

#     weekend = models.BooleanField(default=False, help_text="Weekdays or Weekend")

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self) -> str:
#         return f"Offhours schedule by {self.owner}"
    
