from datetime import time
from django.db import models
from .choices import (
    PIN_CHOICES,
    ZONE_PIN_CHOICES,
    IONIQ_LOAD_TYPES,
    IONIQ_TYPES,
    HEATING_SENSOR_TYPES,
    HEATING_SENSOR_PIPES,
    BOILER_TYPES,
    BOILER_SYSHEALTH_STATUSES,
    BOILER_FORCED_STATES,
)
from devices.utils import dao
from django_q.tasks import async_task


class DeviceAbstractModel(models.Model):
    class Meta:
        abstract = True

    serial_num = models.CharField(max_length=60, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class IoniqControllerModel(DeviceAbstractModel):
    class Meta:
        verbose_name = "Ioniq controller"
        verbose_name_plural = "Ioniq controllers"
        ordering = ["-created_at"]

    owner = models.ForeignKey(
        "users.OwnerProfileModel",
        on_delete=models.PROTECT,
        related_name="ioniq_controllers",
        related_query_name="ioniq_controller",
        null=True,
        blank=True,
        help_text="Related property Owner",
    )

    building = models.ForeignKey(
        "properties.BuildingModel",
        on_delete=models.SET_NULL,
        related_name="ioniq_controllers",
        related_query_name="ioniq_controller",
        null=True,
        help_text="Place of installation",
    )

    model_type = models.CharField(
        max_length=2,
        choices=IONIQ_TYPES,
        default="",
    )

    is_master = models.BooleanField(
        default=True,
        help_text="Check this field if this is a master controller. Otherwise, it will be considered as slave",
    )

    systemp_correction_index = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="IoniqMini systemp correction index (In case of Max, look for sensor model)",
    )

    load_type = models.CharField(
        max_length=3,
        choices=IONIQ_LOAD_TYPES,
        default="",
    )

    boiler = models.ForeignKey(
        "devices.BoilerModel",
        on_delete=models.PROTECT,
        related_name="ioniq_controllers",
        related_query_name="ioniq_controller",
        null=True,
        blank=True,
        help_text="Connected Boiler",
    )

    def __str__(self) -> str:
        return f"Ioniq #{self.serial_num} {self.building}"


class SmartThermostatModel(DeviceAbstractModel):
    class Meta:
        verbose_name = "Smart thermostat"
        verbose_name_plural = "Smart thermostats"
        ordering = ["-created_at"]

    name = models.CharField(max_length=120, default="", blank=True)
    zone = models.ForeignKey(
        "properties.ZoneModel",
        on_delete=models.SET_NULL,
        related_name="smart_thermostats",
        related_query_name="smart_thermostat",
        null=True,
        blank=True,
        help_text="Related property Heating Zone",
    )

    pin_num = models.SmallIntegerField(
        choices=PIN_CHOICES, null=True, help_text="pin connection index"
    )

    owner = models.ForeignKey(
        "users.OwnerProfileModel",
        on_delete=models.PROTECT,
        related_name="smart_thermostats",
        related_query_name="smart_thermostat",
        null=True,
        blank=True,
        help_text="Related property Owner",
    )

    last_set_temperature = models.SmallIntegerField(
        null=True,
        blank=True,
        help_text="Field for storing last set temp value before switching off by the owner",
    )

    set_temperature = models.SmallIntegerField(
        null=True,
        blank=True,
        help_text="Field for storing thermostat owner command set temperature value",
        default=38,
    )

    status = models.BooleanField(default=True)
    scheduled_override = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.set_temperature != 39:
            self.last_set_temperature = self.set_temperature

        super().save(*args, **kwargs)  # Call the "real" save() method.

    def __str__(self) -> str:
        return f"Thermostat: #{self.serial_num} | zone: {self.zone.name if self.zone is not None else 'Undefined'}"


class AnalogueThermostatModel(DeviceAbstractModel):
    class Meta:
        verbose_name = "Analogue thermostat"
        verbose_name_plural = "Analogue thermostats"
        ordering = ["-created_at"]

    # serial_num = None
    make = models.CharField(max_length=60, default="", blank=True)
    model = models.CharField(max_length=60, default="", blank=True)

    pin_num = models.SmallIntegerField(
        choices=ZONE_PIN_CHOICES, null=True, help_text="pin connection index"
    )

    status = models.BooleanField(default=False)
    scheduled_override = models.BooleanField(default=False)

    zone = models.ForeignKey(
        "properties.ZoneModel",
        on_delete=models.SET_NULL,
        related_name="analogue_thermostats",
        related_query_name="analogue_thermostat",
        null=True,
        help_text="Related Heating Zone",
    )

    def __str__(self) -> str:
        return f"[A] Thermostat | pin #{self.pin_num} zone:  {self.zone.name if self.zone is not None else 'Undefined'}"


class SimpleSwitchModel(DeviceAbstractModel):
    class Meta:
        verbose_name = "Heat switch"
        verbose_name_plural = "Heat switchers"
        ordering = ["-created_at"]

    pin_num = models.SmallIntegerField(
        choices=ZONE_PIN_CHOICES, null=True, help_text="pin connection index"
    )

    zone = models.ForeignKey(
        "properties.ZoneModel",
        on_delete=models.SET_NULL,
        related_name="simple_switches",
        related_query_name="simple_switch",
        null=True,
        help_text="Related Heating Zone",
    )

    status = models.BooleanField(default=True)
    scheduled_override = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Heat switch | {self.serial_num} | zone:  {self.zone.name if self.zone is not None else 'Undefined'}"


class SensorModel(DeviceAbstractModel):
    class Meta:
        verbose_name = "Sensor"
        verbose_name_plural = "Sensors"
        ordering = ["-created_at"]

    parent_device = models.ForeignKey(
        IoniqControllerModel,
        on_delete=models.CASCADE,
        related_name="sensors",
        related_query_name="sensor",
        help_text="Parent controller",
    )

    zone = models.ForeignKey(
        "properties.ZoneModel",
        on_delete=models.SET_NULL,
        related_name="sensors",
        related_query_name="sensor",
        null=True,
        blank=True,
        help_text="Related property Zone",
    )

    pin_num = models.SmallIntegerField(
        null=True,
        blank=True,
        choices=PIN_CHOICES,
        help_text="PIN number used with Controller sensor connection",
    )

    zone_pin = models.SmallIntegerField(
        null=True,
        blank=True,
        choices=PIN_CHOICES,
        help_text="PIN number used with Controller zone connection",
    )

    type = models.CharField(
        max_length=3,
        choices=HEATING_SENSOR_TYPES,
        default="",
    )

    correction_index = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Correction value for temperature sensor reading (positive/negative)",
    )

    is_system = models.BooleanField(
        default=False,
        help_text="Check this if current sensor installed in the main heating loop",
    )

    pipe = models.CharField(
        max_length=3,
        choices=HEATING_SENSOR_PIPES,
        default="",
        blank=True,
    )

    def __str__(self) -> str:
        return f"Sensor #{self.serial_num} type: {self.get_type_display()} | controller: {self.parent_device.serial_num}"


class BoilerModel(DeviceAbstractModel):
    class Meta:
        verbose_name = "Boiler"
        verbose_name_plural = "Boilers"
        ordering = ["-created_at"]

    model = models.CharField(max_length=60, default="", blank=True)

    owner = models.ForeignKey(
        "users.OwnerProfileModel",
        on_delete=models.CASCADE,
        related_name="boilers",
        related_query_name="boiler",
        null=True,
        blank=True,
        help_text="Related property Owner",
    )

    type = models.PositiveSmallIntegerField(
        choices=BOILER_TYPES,
        default=0,
    )

    installation_date = models.DateField(null=True, auto_now_add=True)
    shower_duration = models.SmallIntegerField(null=True, blank=True)

    shutdown_temp = models.IntegerField(
        null=True, blank=True, default=55, help_text="Warm weather shutdown setpoint"
    )

    weekdays_offhours_setpoint = models.SmallIntegerField(
        null=True,
        blank=True,
        default=55,
        help_text="Set temperature for non-working hours weekend",
    )

    weekdays_offhours_start_time = models.TimeField(
        null=True, blank=True, default=time(19, 0, 0)
    )
    weekdays_offhours_end_time = models.TimeField(
        null=True, blank=True, default=time(7, 0, 0)
    )

    weekdays_offhours_enabled = models.BooleanField(default=False)

    weekend_offhours_setpoint = models.SmallIntegerField(
        null=True,
        blank=True,
        default=55,
        help_text="Set temperature for non-working hours weekend",
    )

    weekend_offhours_start_time = models.TimeField(null=True, blank=True)
    weekend_offhours_end_time = models.TimeField(null=True, blank=True)

    weekend_offhours_enabled = models.BooleanField(default=False)

    vacant_setpoint = models.SmallIntegerField(
        null=True,
        blank=True,
        default=50,
        help_text="Set temperature for non-working hours",
    )

    away_mode_enabled = models.BooleanField(default=False, help_text="*Away* mode")

    shutdown_enabled = models.BooleanField(
        default=False, help_text="Might be enabled by the property owner"
    )

    shutdown_active = models.BooleanField(
        default=False,
        help_text="If the backend logic activated wwsd on its own based on weather API",
    )

    # Heating cycles optimization mode
    heating_optmode = models.BooleanField(
        default=False,
        help_text="Enables automated heating cycles optimization, based on max systemp settings and return pipe min delta",
    )

    systemp_limit = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Sets maximum systemp value in F, which will cause endswitch turn off",
    )

    cold_pipe_delta_t = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Sets minimum temperature delta value which restricts cold pipe temp drop up to 140 F (i.e. delta_t = 10, minim temp = 150 F)",
    )

    # Manual override state
    forced_endswitch_state = models.PositiveSmallIntegerField(
        choices=BOILER_FORCED_STATES, default=2, help_text="Affects IoniqMini API only"
    )

    health_status = models.CharField(
        max_length=3,
        choices=BOILER_SYSHEALTH_STATUSES,
        default="",
        help_text="Boiler's system health status",
    )

    # def save(self, *args, **kwargs):
    #     controller = self.ioniq_controllers.first()
    #     if controller is not None:
    #         payload = {
    #             "shutdown_temp": self.shutdown_temp,
    #             "shutdown_enabled": int(self.shutdown_enabled),
    #             "shutdown_active": int(self.shutdown_active),
    #             "heating_optmode": int(self.heating_optmode),
    #             "systemp_limit": self.systemp_limit,
    #             "cold_pipe_delta_t": self.cold_pipe_delta_t,
    #             "forced_endswitch_state": self.forced_endswitch_state,
    #             "vacant_setpoint": self.vacant_setpoint,
    #             "away_mode_enabled": int(self.away_mode_enabled),
    #             "sn": controller.serial_num,
    #         }
    #         async_task("devices.utils.dao.save_boiler_controller_settings", payload)
    #     super().save(*args, **kwargs)  # Call the parent save() method.

    def __str__(self) -> str:
        return f"Boiler #{self.serial_num}"
