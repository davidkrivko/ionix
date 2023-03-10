from devices.models import BoilerModel
from schedules.models import DeviceScheduleModel
from properties.models import ApartmentModel, RoomModel, ZipCodeModel
from django_q.tasks import async_iter, async_task
from django.utils import timezone
import logging

from users.models import TenantProfileModel

now = timezone.now


### WWSD LOGIC

def trigger_warm_weather_shutdown_check():
    """Scheduled taks after weather API update
    """
    # So the outdoor temp update arrived, let's check all the buidlings withing each zip

    iter = [obj.pk for obj in ZipCodeModel.objects.all()]
    async_iter('workers.tasks.check_boiler_settings', iter)


def check_boiler_settings(zip_pk: int):
    """
    Fetches all buildings/boilers
    and checks their wwsd settings
    """
    print("Running boiler settings check")
    try:
        zip = ZipCodeModel.objects.get(pk=zip_pk)
    except:
        logging.warning("zip code object scheduled for WWSD status check not found")
        return

    buildings = zip.buildings.all()
    for building in buildings:

        # boiler_rooms = building.boiler_rooms.all()
        # for boiler_room in boiler_rooms:
        #     boiler = boiler_room.boiler
        if building.boiler.shutdown_enabled is True:
            # trigger actual comparator function and endswitch tooggler
            async_task('workers.tasks.check_actuality_data', building.boiler.pk, zip_pk)
    return "OK"


# def toggle_warm_weather_shutdown(boiler_pk: int, zip_pk: int):
#     """
#     Disable or enable endswitch if owner have enabled
#     automatic warm weather shutdown mode and current
#     outdoor temperature has changed.
#     """
#     zip_model = ZipCodeModel.objects.get(pk=zip_pk)
#     boiler = BoilerModel.objects.get(pk=boiler_pk)
#     shutdown_temp = boiler.shutdown_temp  # Current settings for the shutdown temp
#     outdoor_temp = zip_model.todays_temp  # Last update from the weather API
#     update_date = zip_model.updated_at.date()
#     controller = boiler.ioniq_controllers.first()
#     value = 2  # set to autonomous work by default
#
#     # bool
#     is_freshy = update_date == now().date()  # NB change this to timedelta
#     if not is_freshy:
#         logging.warning("Weather API update is not fresh, please troubleshoot the api")
#         async_task('devices.utils.switch_boiler_supply', controller.serial_num, value)
#         return "Did nothing, weather api is dead"
#
#     if outdoor_temp >= shutdown_temp:
#         # set endswitch to offline
#         boiler.shutdown_active = True
#         value = 0
#     if outdoor_temp < shutdown_temp:
#         boiler.shutdown_active = False
#         value = 2
#     # update device variables [blr] for IoniqMax
#     async_task('devices.utils.switch_boiler_supply', controller.serial_num, value)
#     boiler.save()
#
#     return ("Boiler WWSD status:", value)


def check_actuality_data(boiler_pk: int, zip_pk: int):
    zip_model = ZipCodeModel.objects.get(pk=zip_pk)
    boiler = BoilerModel.objects.get(pk=boiler_pk)
    shutdown_temp = boiler.shutdown_temp  # Current settings for the shutdown temp
    update_date = zip_model.updated_at.date()
    controller = boiler.ioniq_controllers.first()
    value = 2

    is_actual = update_date == now().date()
    if not is_actual:
        try:
            async_task("workers.workers.update_weather_on_zips")
        except:
            logging.warning("ZIP code is invalid")
    if zip_model.todays_temp >= shutdown_temp:
        boiler.shutdown_active = True
        value = 0
    if zip_model.todays_temp < shutdown_temp:
        boiler.shutdown_active = False
        value = 2

    payload = {
        "wwsd": value
    }
    async_task("streams.daos.set_boiler_data", controller, payload)
    boiler.save()

    return ("Boiler WWSD status:", value)


# SCHEDULE TASK WORKERS
def reset_thermostat_with_schedule(schedule_pk: int):
    """
    Background task run by the scheduled worker.
    Resets all subscribed smart thermostats according to the
    schedule settings.
    """
    schedule_list = DeviceScheduleModel.objects.get(pk=schedule_pk)
    try:
        subscribers = schedule_list.subscribers.select_related("thermostat")
    except:
        # No subbscribers? Do nothing
        return
    for subscriber in subscribers.iterator():
        thermostat = subscriber.thermostat
        thermostat.set_temperature = subscriber.setpoint
        thermostat.scheduled_override = True
        thermostat.save()


def reset_switches_with_schedule(schedule_pk: int):
    """
    Background task run by the scheduled worker.
    Resets all subscribed simple heatswitches according to the
    schedule settings.
    """
    schedule_list = DeviceScheduleModel.objects.get(pk=schedule_pk)
    try:
        subscribers = schedule_list.heat_switches.select_related("switch")
    except:
        # No subbscribers? Do nothing
        return
    for subscriber in subscribers.iterator():
        switch = subscriber.switch
        switch.status = subscriber.status
        switch.scheduled_override = True
        switch.save()


def reset_analogue_thermostats_with_schedule(schedule_pk: int):
    """
    Background task run by the scheduled worker.
    Resets all subscribed analogue thermostats according to the
    schedule settings.
    """
    schedule_list = DeviceScheduleModel.objects.get(pk=schedule_pk)
    try:
        subscribers = schedule_list.analogue_switches.select_related("analogue_thermostat")
    except:
        # No subbscribers? Do nothing
        return
    for subscriber in subscribers.iterator():
        analogue_thermostat = subscriber.analogue_thermostat
        analogue_thermostat.status = subscriber.status
        analogue_thermostat.scheduled_override = True
        analogue_thermostat.save()


def process_vacant_apartment(apartment_id: int):
    """
    Async task which removes room related tenant accounts and resets
    smart thermostat setpoint according to boiler settings
    (landlord settings)
    """
    # print("Processing vacant apartment")
    apartment = ApartmentModel.objects.get(pk=apartment_id)
    rooms_queryset = apartment.rooms.all()
    try:
        vacant_apartment_setpoint = apartment.boiler.vacant_setpoint
    except:
        vacant_apartment_setpoint = None
    # print("vacant_apartment_setpoint", vacant_apartment_setpoint)

    # Shared access clean up
    if rooms_queryset.exists():
        # print("rooms_queryset.exists():", rooms_queryset.exists())
        for room in rooms_queryset:
            tenants_queryset = room.tenants.all()
            if tenants_queryset.exists():
                # print("tenants_queryset.exists()", tenants_queryset.exists())
                for tenant in tenants_queryset:
                    # print("tenant", tenant)
                    user = tenant.user
                    user.delete()
                    # remove tenant profile by cascade

            # Thermostats processing
            smart_thermostat = room.thermostat
            if room.thermostat is not None and vacant_apartment_setpoint is not None:
                smart_thermostat.set_temperature = vacant_apartment_setpoint
                smart_thermostat.save()

    return "OK"


def apartment_occupied_now(tenant_id: int):
    """
    Async task to switch apartment back to occupied
    status after new tenant arrived (being created)
    """
    try:
        tenant = TenantProfileModel.objects.get(pk=tenant_id)
        room = tenant.rooms.first()
    except:
        return "Room not found"
    apartment = room.apartment
    apartment.is_vacant = False
    apartment.save()
