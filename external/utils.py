import logging
from django_q.tasks import async_task
from devices.models import (
    SmartThermostatModel,
    IoniqControllerModel,
)
from devices.utils import (
    get_thermostat_data,
    switch_boiler_supply,
    change_device_variables,
)
from streams.utils import fetch_online_status_from_online_stream
from django.utils.timezone import now
from django.utils import dateparse

# from streams.daos import RedisDao
from devices.utils import dao


def process_ioniq_max_with_related_thermostats(serial_num: str) -> int:
    """Fetches 'relay' data from related thermostats (within same heating zone)
    and returns state for endswitch.

    Args:
        serial_num (str): device serial number

    Returns:
        int: 1 or 2 - for blr/endswitch status change (on or auto)
    """
    endswitch_response = 2

    rel_thermostats_serial_nums = dao.get_max_controller_related_thermostats(
        sn=serial_num
    )

    if len(rel_thermostats_serial_nums) == 0:
        rel_thermostats_queryset = SmartThermostatModel.objects.filter(
            zone__controller__serial_num=serial_num
        )
        if not rel_thermostats_queryset.exists():
            return endswitch_response

        rel_thermostats_serial_nums_db = list(
            rel_thermostats_queryset.values_list("serial_num", flat=True)
        )
        rel_thermostats_serial_nums = rel_thermostats_serial_nums_db

        # print("rel_thermostats_serial_nums_db", rel_thermostats_serial_nums_db)
        dao.set_max_controller_related_thermostats(
            sn=serial_num, thermostats_serials=rel_thermostats_serial_nums_db
        )

    for thermostat_sn in rel_thermostats_serial_nums:
        therm_data = dao.get_paired_thermostat_data(sn=thermostat_sn)

        if therm_data is None:
            continue

        time_delta = now() - dateparse.parse_datetime(therm_data["timestamp"])

        if int(therm_data["relay"]) == 1 and time_delta.seconds <= 120:
            endswitch_response = 1

    return endswitch_response


def get_thermostat_set_point(serial_num: str) -> int:
    try:
        thermostat = SmartThermostatModel.objects.get(serial_num=serial_num)
    except:
        return None

    set_temperature = thermostat.set_temperature

    return set_temperature


def calculate_ioniqmini_response(serial_num: str) -> bool:
    """Compares smart thermostats and heat switch states
    to retun on/off response to the following Ioniq API request
    """

    ioniq = IoniqControllerModel.objects.prefetch_related("boiler").get(
        serial_num=serial_num
    )

    final = False
    errors = None

    try:
        boiler = ioniq.boiler
    except:
        errors = "No boilers attached"

    # First priority check if boiler has forces endswitch state active
    if boiler.forced_endswitch_state == 2:
        pass
    elif boiler.forced_endswitch_state == 1:
        return (True, None)
    else:
        return (False, None)

    # Second Priority check if warm weather shutdown switched off the boiler
    shutdown_active = boiler.shutdown_active
    if shutdown_active:
        return (False, None)

    # If shutdown_active is false perform other status checks among thermostats
    # (call for heat statuese)
    try:
        if ioniq.zones.exists():
            for zone in ioniq.zones.all():
                if zone.smart_thermostats.exists():
                    for thermostat in zone.smart_thermostats.all():
                        data = get_thermostat_data(thermostat.serial_num)
                        status = fetch_online_status_from_online_stream(
                            thermostat.serial_num, device="TRM"
                        )
                        if len(data) > 0:
                            # print("data[0]['status']", data[0]['status'])
                            # print("thermostat.serial_num", thermostat.serial_num)
                            if data[0]["status"] == 1 and status["data"] == True:
                                final = True

                if zone.simple_switches.exists():
                    for switch in zone.simple_switches.all():
                        if switch.status == True:
                            # print("switch.status", switch.status)
                            final = True
    except Exception as e:
        errors = str(e)

    return (final, errors)


def update_device_variables_smart_max(serial_num: str, status: int):
    """If smart thermostat connected to IoniqMax
    updates device variables in IoT db

    Args:
        serial_num (str): ioniq serial number
        status (int): smart thermostat status update (1-call for heat, 0-idle)
    """
    # print("Checking if variables update needed")

    try:
        smart_thermostat = SmartThermostatModel.objects.get(serial_num=serial_num)
    except:
        logging.warning("Unable to find thermostat object with serial number specified")
        return

    # Check if we're dealing with IoniqMax connection
    try:
        controller = smart_thermostat.zone.controller
    except:
        logging.info("Controller connection not found")
        return

    if controller.model_type == "MX":
        async_task(
            "devices.utils.change_device_variables",
            controller.serial_num,
            smart_thermostat.pin_num,
            status,
        )


def heating_optimization_utility(payload: dict):
    """
    Processes API incoming data and toggles endswitch variable if
    optimization mode is enabled on attached boiler
    Args:
        serial_num (str): ioniqmax controller serial num
        payload (dict): t1, t2, t3, endswitch data
    """
    serial_num = payload["sn"]
    boiler_data = dao.get_boiler_controller_settings(serial_num)
    print("boiler_data", boiler_data)

    if boiler_data is not None:
        systemp_limit = int(boiler_data["systemp_limit"])
        cold_pipe_delta_t = int(boiler_data["cold_pipe_delta_t"])
        heating_optmode = True if int(boiler_data["heating_optmode"]) == 1 else False
        print("heating_optmode", heating_optmode)
    else:
        print("Hitting database!")
        try:
            controller = IoniqControllerModel.objects.select_related("boiler").get(
                serial_num=serial_num, is_master=True, boiler__isnull=False
            )
        except:
            return
        try:
            boiler = controller.boiler
        except:
            return

        systemp_limit = boiler.systemp_limit
        cold_pipe_delta_t = boiler.cold_pipe_delta_t
        heating_optmode = boiler.heating_optmode

    if not heating_optmode:
        # do nothing
        print("heating_optmode is off")
        return
    print("Proceeding")
    if systemp_limit is None or cold_pipe_delta_t is None:
        # do nothing
        return

    cold_pipe_t = payload["t1"]
    systemp = payload["t2"]
    # hot_pipe_t = payload['t3']

    min_cold_pipe_temp = 140

    # 1 Check if cold pipe temperature reached the limit
    if cold_pipe_t <= min_cold_pipe_temp + cold_pipe_delta_t:
        # set endswitch / blr 1 var
        # switch_boiler_supply(serial_num, 2)
        change_device_variables(serial_num, 1, 1)

    elif systemp >= systemp_limit:
        # set blr to 0
        # switch_boiler_supply(serial_num, 0)
        change_device_variables(serial_num, 1, 0)
    else:
        pass

    return True
