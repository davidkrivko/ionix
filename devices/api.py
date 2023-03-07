from datetime import timezone
from django_q.tasks import async_task
from rest_framework import generics, mixins, viewsets
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .utils import (
    get_thermostat_data,
    fetch_ioniq_data,
    fetch_devicezone_status,
)
from .serializers import (
    SetTempCommandSerializer,
    DeviceStatusSerializer,
    HeatSwitchStatusSerializer,
    BoilerModelSerializer,
    BoilerShutDownTempSerializer,
    DeviceIdSerializer,
    SmartThermostatModelSerializer,
    NameFieldSerializer,
    BoilerHealthStatusSerializer,
)
from .models import (
    AnalogueThermostatModel,
    IoniqControllerModel,
    SmartThermostatModel,
    SimpleSwitchModel,
    BoilerModel,
)
from django.conf import settings
from django.utils import timezone
from streams.utils import fetch_online_status_from_online_stream
from streams.daos import redis_dao
import logging

now = timezone.now

DEVICE_ONLINE_STATUS_DELTA_SEC = settings.DEVICE_ONLINE_STATUS_DELTA_SEC


# @ SIMPLE THERMOSTAT CONTROL PAGE API
class OwnSmartThermostatsList(ListAPIView):

    serializer_class = SmartThermostatModelSerializer
    permission_classses = [IsAuthenticated]

    def get_queryset(self):
        owner = self.request.user.owner
        queryset = SmartThermostatModel.objects.filter(owner=owner).order_by("name")
        return queryset


class GetThermostatDataFromStream(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        thermostat_serial = self.kwargs.get("serial")
        try:
            SmartThermostatModel.objects.get(
                serial_num=thermostat_serial, owner=self.request.user.owner
            )
        except Exception as exc:
            logging.warning("Error checking thermostat data ownership %s", exc)
            return Response(status=403)

        try:
            data = redis_dao.get_paired_thermostat_data(sn=thermostat_serial)
            # print("data", data)s
        except Exception as exc:
            logging.warning(exc)
            return Response(status=200)

        try:
            data.pop("token", None)
        except Exception:
            pass
        return Response(data, status=200)


class GetControllerDataFromStream(APIView):

    permission_classses = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        controller_serial = self.kwargs.get("serial")
        try:
            data = redis_dao.get_paired_relay_controller_data(sn=controller_serial)
            # print("data", data)
        except Exception as exc:
            logging.warning(exc)
            return Response(status=200)

        try:
            data.pop("token", None)
        except Exception:
            pass
        return Response(data, status=200)


class ThermostatNameUpdateView(APIView):
    """Allow onwers to update thermostat name"""

    permission_classses = [IsAuthenticated]

    def post(self, *args, **kwargs):

        thermostat_pk = self.kwargs.get("thermostat_pk")
        try:
            thermostat = SmartThermostatModel.objects.get(pk=thermostat_pk)
        except Exception as exc:
            return Response(status=404)

        serializer = NameFieldSerializer(data=self.request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            thermostat.name = name
            thermostat.save()
            return Response(status=200)


class ThermostatDataApiView(APIView):
    """Parses all thermostats belonging
    to the current user with owner profile

    Args:
        APIView ([type]): [description]
    """

    def get(self, request):
        ctx = {
            "detail": None,
            "data": None,
        }

        thermostats_queryset = request.user.owner.smart_thermostats.all()

        if thermostats_queryset.exists():
            thermostat_data = []
            for thermostat in thermostats_queryset:
                serial_num = thermostat.serial_num
                data = get_thermostat_data(serial_num)
                thermostat_data.append(data)

            ctx["data"] = thermostat_data

        return Response(ctx, status=200)


class ThermostatDataBySerialNumber(APIView):
    """Parse thermostat data with s/n

    Args:
        APIView ([type]): [description]
    """

    def post(self, request):
        ctx = {
            "detail": None,
            "data": None,
        }
        serializer = DeviceStatusSerializer(data=request.data)
        if serializer.is_valid():
            sn = serializer.validated_data.get("sn")

            data = get_thermostat_data(sn)

            ctx["data"] = data

            return Response(ctx, status=200)

        ctx["detail"] = serializer.error_messages

        return Response(ctx, status=500)


class ThermostatSetTemperatureApiView(APIView):
    """Allow thermostat owner to write set temperature
    value/command
    """

    def post(self, request):
        ctx = {"detail": None, "data": None}
        serializer = SetTempCommandSerializer(data=request.data)

        if serializer.is_valid():
            thermostat_sn = serializer.validated_data.get("thermostat_sn")
            set_temperature = serializer.validated_data.get("set_temperature")
            status = serializer.validated_data.get("status")

            try:
                thermostat = SmartThermostatModel.objects.get(
                    serial_num=thermostat_sn, owner=self.request.user.owner
                )
            except:
                ctx["detail"] = "Thermostat with serial number specified not found"
                return Response(ctx, status=404)

            # N/B ADD PERMISSION CHECK FOR BOTHER OWNER AND TENANT ROLES

            if set_temperature is None:
                ctx["detail"] = "Bad data"
                return Response(ctx, status=400)

            thermostat.set_temperature = set_temperature
            thermostat.scheduled_override = False
            if status is not None:
                thermostat.status = status

            redis_dao.set_thermostat_setpoint(
                sn=thermostat_sn, setpoint=str(set_temperature)
            )
            thermostat.save()

            ctx["detail"] = "Tempereture setpoint was successfully saved"

            return Response(ctx, status=200)
        else:
            ctx["detail"] = serializer.error_messages
            return Response(ctx, status=500)


class GetLastSetpointApiView(APIView):
    """Allow UI component to fetch setpoint value
    directly from django model (settings approach)
    """

    def post(self, request):
        ctx = {"detail": None, "data": None}
        serializer = DeviceStatusSerializer(data=request.data)

        if serializer.is_valid():
            sn = serializer.validated_data.get("sn")
            try:
                thermostat = SmartThermostatModel.objects.get(serial_num=sn)
            except:
                ctx["detail"] = "Devices with serial number specified not found"
                return Response(ctx, status=404)

            ctx["data"] = {
                "set_temperature": thermostat.set_temperature,
                "last_set_temperature": thermostat.last_set_temperature,
                "status": thermostat.status,
                "sheduled_override": thermostat.scheduled_override,
            }
            return Response(ctx, status=200)


class RetriveThermostatLastStatusApiView(APIView):
    """Allows parsing thermostat last status update
    from redis stream
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        # ctx = {
        #     'detail': None,
        #     'data': None,
        # }
        serializer = DeviceStatusSerializer(data=request.data)

        if serializer.is_valid():
            sn = serializer.validated_data.get("sn")
            ctx = fetch_online_status_from_online_stream(sn, "TRM")
            return Response(ctx, status=200)


class RetriveIoniqLastStatusApiView(APIView):
    """Allows parsing ioniq last status update
    from redis stream
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = DeviceStatusSerializer(data=request.data)

        if serializer.is_valid():
            sn = serializer.validated_data.get("sn")
            ctx = fetch_online_status_from_online_stream(sn, "ION")
            return Response(ctx, status=200)


class RetriveThermostatControllerStatusApiView(APIView):
    """Allows parsing ioniq last status update
    from redis stream based on thermostan serial
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        ctx = {
            "detail": None,
            "data": None,
        }
        serializer = DeviceStatusSerializer(data=request.data)

        if serializer.is_valid():
            thermostat_sn = serializer.validated_data.get("sn")
            try:
                smart_thermostat = SmartThermostatModel.objects.get(
                    serial_num=thermostat_sn
                )
            except:
                ctx["detail"] = "Thermostat with serial number specified not found"
                return Response(ctx, status=404)
            try:
                controller = smart_thermostat.zone.controller
            except:
                ctx[
                    "detail"
                ] = "Heating zone configuration doesn't have controller connected"
                return Response(ctx, status=404)

            ctx = fetch_online_status_from_online_stream(controller.serial_num, "ION")
            return Response(ctx, status=200)


class RetriveHeatSwitchControllerStatusApiView(APIView):
    """Allows parsing ioniq last status update
    from redis stream based on heat switch serial
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        ctx = {
            "detail": None,
            "data": None,
        }
        serializer = DeviceStatusSerializer(data=request.data)

        if serializer.is_valid():
            thermostat_sn = serializer.validated_data.get("sn")
            try:
                heat_switch = SimpleSwitchModel.objects.get(serial_num=thermostat_sn)
            except:
                ctx["detail"] = "Heat switch with serial number specified not found"
                return Response(ctx, status=404)
            try:
                controller = heat_switch.zone.controller
            except:
                ctx[
                    "detail"
                ] = "Heating zone configuration doesn't have controller connected"
                return Response(ctx, status=404)

            ctx = fetch_online_status_from_online_stream(controller.serial_num, "ION")
            return Response(ctx, status=200)


class RetriveAnalogueThermostatControllerStatusApiView(APIView):
    """Allows parsing ioniq last status update
    from redis stream based on analogue thermostat serial
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        ctx = {
            "detail": None,
            "data": None,
        }
        serializer = DeviceStatusSerializer(data=request.data)

        if serializer.is_valid():
            thermostat_sn = serializer.validated_data.get("sn")
            try:
                analogue_thermostat = AnalogueThermostatModel.objects.get(
                    serial_num=thermostat_sn
                )
            except:
                ctx[
                    "detail"
                ] = "Analogue thermostat with serial number specified not found"
                return Response(ctx, status=404)
            try:
                controller = analogue_thermostat.zone.controller
            except:
                ctx[
                    "detail"
                ] = "Heating zone configuration doesn't have controller connected"
                return Response(ctx, status=404)

            ctx = fetch_online_status_from_online_stream(controller.serial_num, "ION")
            return Response(ctx, status=200)


class RetrieveIoniqDataApiView(APIView):
    """Allows frontend to fetch data
    from ioniq mini/max tables
    """

    # permission_classes = [IsAuthenticated]

    def post(self, request):
        ctx = {"detail": None, "data": None}
        serializer = DeviceStatusSerializer(data=request.data)

        if serializer.is_valid():

            sn = serializer.validated_data.get("sn")
            try:
                smart_thermostat = SmartThermostatModel.objects.get(serial_num=sn)
            except:
                ctx["detail"] = "Thermostat with serial number specified not found"
                return Response(ctx, status=404)
            try:
                controller = smart_thermostat.zone.controller
            except:
                ctx[
                    "detail"
                ] = "Heating zone configuration doesn't have controller connected"
                return Response(ctx, status=404)

            if controller.model_type == "MX":
                data = fetch_ioniq_data(controller.serial_num, extended=True)
                ctx["data"] = data

            if controller.model_type == "MN":
                data = fetch_ioniq_data(controller.serial_num, extended=False)
                ctx["data"] = data

            return Response(ctx, status=200)


# NB and permissions check
class HeatSwitchStatusUpdateApiView(APIView):
    """Allow heat switcher status update
    for tenants and owners
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        ctx = {"detail": None, "data": None}
        serializer = HeatSwitchStatusSerializer(data=request.data)

        if serializer.is_valid():

            id = serializer.validated_data.get("id")
            status = serializer.validated_data.get("status")

            try:
                switch = SimpleSwitchModel.objects.get(pk=id)
            except:
                ctx["detail"] = "Simple switch with specified Id not found"
                return Response(ctx, status=404)

            switch.status = status
            switch.save()

            ctx["detail"] = "Switch status was successfully updated"
            return Response(ctx, status=200)
        else:
            ctx["detail"] = serializer.error_messages
            return Response(ctx, status=400)


# NB and permissions check
class AnalogueThermostatStatusUpdateApiView(APIView):
    """Allow heat switcher status update
    for tenants and owners
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        ctx = {"detail": None, "data": None}
        # Reusing same serializer
        serializer = HeatSwitchStatusSerializer(data=request.data)

        if serializer.is_valid():

            id = serializer.validated_data.get("id")
            status = serializer.validated_data.get("status")

            try:
                thermostat = AnalogueThermostatModel.objects.get(pk=id)
            except:
                ctx["detail"] = "Analogue thermostat with specified Id not found"
                return Response(ctx, status=404)

            thermostat.status = status
            thermostat.save()

            ctx["detail"] = "Analogue thermostat status was successfully updated"
            return Response(ctx, status=200)
        else:
            ctx["detail"] = serializer.error_messages
            return Response(ctx, status=400)


class RetrieveDeviceZoneStatusApiView(APIView):
    """Allow API client request device zone status
    based on device serial number
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DeviceStatusSerializer(data=request.data)
        ctx = {"detail": None, "data": None}
        if serializer.is_valid():
            sn = serializer.validated_data.get("sn")
            device_type = serializer.validated_data.get("device_type")

            if device_type == "heat_switch":
                try:
                    device = SimpleSwitchModel.objects.get(serial_num=sn)
                    controller = device.zone.controller
                except:
                    return Response(status=404)
            if device_type == "analogue":
                try:
                    device = AnalogueThermostatModel.objects.get(serial_num=sn)
                    controller = device.zone.controller
                except:
                    return Response(status=404)

            response = fetch_devicezone_status(controller.serial_num, device.pin_num)

            if response is not None:
                if response["time"].date() == now().date():
                    ctx["data"] = response["state"]
                else:
                    ctx["data"] = 0

            return Response(ctx, status=200)
        else:
            ctx["detail"] = serializer.error_messages
            return Response(ctx, status=500)


class BoilerHealthStatusView(generics.RetrieveAPIView):
    serializer_class = BoilerHealthStatusSerializer
    lookup_field = "serial_num"

    def get_object(self):
        obj = BoilerModel.objects.get(serial_num=self.kwargs["serial_num"])

        return obj


class BoilerListApiView(ListAPIView):
    """Displays a list of boilers installed
    in the owner's property
    """

    serializer_class = BoilerModelSerializer
    permission_classses = [IsAuthenticated]

    def get_queryset(self):

        try:
            queryset = self.request.user.owner.boilers.all()
        except:
            queryset = BoilerModel.objects.none()

        return queryset


class BoilerUpdateApiView(RetrieveUpdateAPIView):
    """Allow onwers to update boiler and boiler
    related (heating) settings
    """

    serializer_class = BoilerModelSerializer
    permission_classses = [IsAuthenticated]

    def get_queryset(self):
        try:
            queryset = self.request.user.owner.boilers.all()
        except:
            queryset = BoilerModel.objects.none()
        # print("queryset", queryset)

        return queryset

    def perform_update(self, serializer):
        instance = serializer.save()
        forced_state_value = serializer.validated_data.get("forced_endswitch_state")

        # if user updates forces state field --> lookup for Max controller and update cold database
        if forced_state_value is not None:
            controller_queryset = instance.ioniq_controllers.filter(
                model_type="MX", is_master=True
            )

            if controller_queryset.exists():
                controller = controller_queryset.first()
                async_task(
                    "devices.utils.switch_boiler_supply",
                    controller.serial_num,
                    forced_state_value,
                )


class BoilerShutdownTempApiView(APIView):
    """
    WWSD settings endpoint. Allows property owners
    to save their heating settings
    """

    permission_classses = [IsAuthenticated]

    def post(self, request):
        ctx = {"detail": None, "data": None}
        serializer = BoilerShutDownTempSerializer(data=request.data)

        if serializer.is_valid():

            boiler_id = serializer.validated_data.get("boiler_id")
            shutdown_temp = serializer.validated_data.get("shutdown_temp")
            shutdown_enabled = serializer.validated_data.get("shutdown_enabled")
            try:
                boiler = BoilerModel.objects.get(pk=boiler_id)
            except:
                return Response(status=404)

            boiler.shutdown_temp = shutdown_temp
            boiler.shutdown_enabled = shutdown_enabled
            if shutdown_enabled == False:
                # if boiler owner switched WWSD off, set controller to autonomous logic
                controller = boiler.ioniq_controllers.first()
                value = 2
                boiler.shutdown_active = False
                async_task(
                    "devices.utils.switch_boiler_supply", controller.serial_num, value
                )

            else:
                zip_pk = boiler.ioniq_controllers.first().building.zip_code.pk
                print("ZIP pk", zip_pk)
                async_task(
                    "workers.tasks.toggle_warm_weather_shutdown", boiler.pk, zip_pk
                )
                # if WWSD mode is on shutdown_enabled == True, we're scheduling another custom check flow
                # toggle_warm_weather_shutdown(boiler_pk: int, zip_pk: int):
            boiler.save()
            ctx[
                "detail"
            ] = "Warm weather shutdown mode settings were successfully changed"

            return Response(ctx, status=200)
        else:
            return Response(serializer.error_messages, status=500)


class BoilerDataApiView(RetrieveAPIView):
    """Allows fetching boiler status and
    WWSD settings / state
    """

    serializer_class = BoilerModelSerializer

    def get_queryset(self):
        queryset = BoilerModel.objects.all()  # NB add
        return queryset


class RetrieveBoilerEndswitchFromIoniqDataApiView(APIView):
    """Takes boiler id and returns master controller
    endswitch data (boiler activity status)
    """

    def post(self, request):
        ctx = {
            "data": None,
            "detail": None,
        }
        serializer = DeviceIdSerializer(data=request.data)
        if serializer.is_valid():
            id = serializer.validated_data.get("id")
            try:
                boiler = BoilerModel.objects.get(pk=id)
            except:
                ctx["detail"] = "Boiler with specified id not found"
                return Response(ctx, status=404)
            try:
                controller = boiler.ioniq_controllers.get(is_master=True)
            except:
                ctx[
                    "detail"
                ] = "Boiler doesn't have controllers connected or has more that one master controller connected"
                return Response(ctx, status=404)

            if controller.model_type == "MX":
                data = fetch_ioniq_data(controller.serial_num, extended=True)
                if data is not None:
                    ctx["data"] = data
                    ctx["data"]["controller"] = controller.serial_num
                    # ioniqmax doesn't have systemp field / determening one
                    try:
                        sensor = controller.sensors.get(is_system=True)
                        sensor_key = f"t{sensor.pin_num}"
                        correction_index = sensor.correction_index
                        ctx["data"]["systemp"] = data[sensor_key] + correction_index
                    except:
                        ctx["data"]["systemp"] = "--"

            if controller.model_type == "MN":
                data = fetch_ioniq_data(controller.serial_num, extended=False)
                ctx["data"] = data
                if data is not None:
                    ctx["data"]["systemp"] = (
                        ctx["data"]["systemp"] + controller.systemp_correction_index
                    )
                    ctx["data"]["controller"] = controller.serial_num
            return Response(ctx, status=200)
        else:
            return Response(serializer.error_messages, status=400)


def fetch_troubleshooting_data(controllers_queryset):
    """
    Fetches controllers and preprocesses their device
    data for front-end consumption
    """
    obj_list = []

    for controller in controllers_queryset:
        ctx = {
            "detail": None,
            "data": {
                "controller": None,
                "is_master": None,
                "model_type": None,
                "zone_currents": None,
                "pipe_temps": None,
                "system_temp": None,
            },
        }
        # if controller is Max type fetch data from devicedata table
        controller_data = None
        if controller.model_type == "MX":
            controller_data = fetch_ioniq_data(controller.serial_num, extended=True)
            # print("controller_data", controller_data)
            temp_sensors = controller.sensors.filter(type="TMP").prefetch_related(
                "zone"
            )
            current_sensors = controller.sensors.filter(type="CRT").prefetch_related(
                "zone"
            )
            zone_pipes_temperatures = list()
            zones_queryset = controller.zones.all()
            error_messages = list()

            # Collecting supply and return pipes temperatures
            for zone in zones_queryset:
                print("zone", zone)
                obj = {
                    "name": zone.name,
                    "SPL": None,
                    "RTN": None,
                }
                try:
                    supply_sensor = temp_sensors.get(zone=zone, pipe="SPL")
                except Exception as e:
                    error_messages.append(
                        f"Supply sensor configuration not defined for zone: {zone}"
                    )
                    supply_sensor = None
                try:
                    return_sensor = temp_sensors.get(zone=zone, pipe="RTN")
                except Exception as e:
                    error_messages.append(
                        f"Return sensor configuration not defined for zone: {zone}"
                    )
                    return_sensor = None
                if supply_sensor:
                    supply_key = f"t{supply_sensor.pin_num}"
                    obj["SPL"] = (
                        controller_data[supply_key] + supply_sensor.correction_index
                    )

                if return_sensor:
                    return_key = f"t{return_sensor.pin_num}"
                    obj["RTN"] = (
                        controller_data[return_key] + return_sensor.correction_index
                    )

                zone_pipes_temperatures.append(obj)

            ctx["data"]["pipe_temps"] = zone_pipes_temperatures
            # Collecting system temperature value
            try:
                sytem_temp_sensor = temp_sensors.get(is_system=True)
                sytem_temp_sensor_key = f"t{sytem_temp_sensor.pin_num}"
                ctx["data"]["system_temp"] = (
                    controller_data[sytem_temp_sensor_key]
                    + sytem_temp_sensor.correction_index
                )
            except:
                error_messages.append(
                    "System temperature sensor configuration not defined"
                )

            try:
                icsz1_name = current_sensors.get(zone_pin=1).zone.name
            except:
                error_messages.append(
                    "Current sensor configuration icsz1 for zone pin 1 not defined"
                )
                icsz1_name = None
            try:
                icsz2_name = current_sensors.get(zone_pin=2).zone.name
            except:
                error_messages.append(
                    "Current sensor configuration icsz2 for zone pin 2 not defined"
                )
                icsz2_name = None
            try:
                icsz3_name = current_sensors.get(zone_pin=3).zone.name
            except:
                error_messages.append(
                    "Current sensor configuration icsz3 for zone pin 3 not defined"
                )
                icsz3_name = None

            ctx["data"]["zone_currents"] = {
                "icsz1": icsz1_name,
                "icsz2": icsz2_name,
                "icsz3": icsz3_name,
            }

        if controller.model_type == "MN":
            controller_data = fetch_ioniq_data(controller.serial_num, extended=False)
            if controller_data is not None:
                ctx["data"]["systemp"] = (
                    controller_data["systemp"] + controller.systemp_correction_index
                )

        ctx["data"]["controller"] = controller_data
        ctx["data"]["model_type"] = controller.model_type
        ctx["data"]["is_master"] = controller.is_master
        ctx["detail"] = error_messages
        obj_list.append(ctx)

    return obj_list


class FetchTroubleShootingDataByBoilerApiView(APIView):
    """
    Allow landlors to fetch controller's
    data for troubleshooting settings page
    using boiler id
    """

    def get(self, request, **kwargs):
        owner = None
        obj_list = []
        try:
            owner = request.user.owner
        except:
            return Response(status=403)
        # determine controller

        pk = self.kwargs.get("pk")
        try:
            boiler = BoilerModel.objects.get(pk=pk, owner=owner)
        except:
            return Response(status=404)
        try:
            controllers_queryset = boiler.ioniq_controllers.all()
        except:
            return Response(status=404)

        if controllers_queryset.exists():
            obj_list = fetch_troubleshooting_data(controllers_queryset)
            print("obj_list", obj_list)

        return Response(obj_list, status=200)


class FetchTroubleShootingDataApiView(APIView):
    """Allow home owners to fetch controller's
    data for troubleshooting block
    """

    def get(self, request):
        owner = None
        obj_list = []
        try:
            owner = request.user.owner
        except:
            return Response(status=403)
        # determine controller
        controllers_queryset = IoniqControllerModel.objects.filter(owner=owner)
        if controllers_queryset.exists():
            obj_list = fetch_troubleshooting_data(controllers_queryset)

        return Response(obj_list, status=200)
