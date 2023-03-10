from devices.models import (
    SimpleSwitchModel, 
    AnalogueThermostatModel,
    BoilerModel,
    SmartThermostatModel,
    IoniqControllerModel,
)
from django.db.models.signals import post_save
from django.utils.timezone import now
from django_q.tasks import async_task
from django.dispatch import receiver
from streams.daos import redis_dao
from loguru import logger


@receiver(post_save, sender=SmartThermostatModel)
def trigger_on_application_update(sender, instance, created, **kwargs):
    redis_dao.set_thermostat_setpoint(sn=instance.serial_num, setpoint=instance.set_temperature)


@receiver(post_save, sender=BoilerModel)
def update_boiler_settings_hash(sender, instance, created, **kwargs):
    controller = instance.ioniq_controllers.first()
    if controller is not None:
        # logger.info("Setting boiler type {}", instance.type)
        redis_dao.set_boiler_data(sn=controller.serial_num, payload={
            "wwsd": 1 if instance.shutdown_active else 0,
            "shutdown_temp": instance.shutdown_temp,
            "shutdown_enabled": 1 if instance.shutdown_enabled else 0,
            "shutdown_active": 1 if instance.shutdown_active else 0,
            "boiler_type": instance.type,
            # "heating_optmode": int(instance.heating_optmode),
            # "systemp_limit": instance.systemp_limit,
            # "cold_pipe_delta_t": instance.cold_pipe_delta_t,
            # "forced_endswitch_state": instance.forced_endswitch_state,
            # "vacant_setpoint": instance.vacant_setpoint,
            # "away_mode_enabled": int(instance.away_mode_enabled),
        })
