import logging
from django.http.response import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from ioniqbox.authentication import ServiceTokenAuthentication
from devices.serializers import (
    ThermostatDataSerializser,
    DevinceOnlineRequestSerializer,
)
from devices.models import SmartThermostatModel, IoniqControllerModel
from .serializers import (
    IoniqMaxDataSerializer,
    # IoniqMaxSystemStateSerializer,
    IoniqMaxUpgradeRequestSerializer,
    ControllerRelayPairDataSerializer,
)
from .utils import (
    get_thermostat_set_point,
    calculate_ioniqmini_response,
    # heating_optimization_utility,
    process_ioniq_max_with_related_thermostats,
)
from .serializers import IoniqMiniStatusRequestSerializer
from django.conf import settings
from django.utils import timezone
from django_q.tasks import async_task
from streams.daos import RedisDao
from loguru import logger

now = timezone.now
dao = RedisDao()

THERMOSTAT_TOKEN = settings.THERMOSTAT_TOKEN


# MOCKUP APIs #noqa
class IoniqMaxDataApiView(APIView):
    """
    Ioniq Max mockup API
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = IoniqMaxDataSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            token = serializer.validated_data.get("token")
            sn = serializer.validated_data.get("sn")
            if token != THERMOSTAT_TOKEN:
                return Response("Invalid token", status=403)
            endswitch = process_ioniq_max_with_related_thermostats(serial_num=sn)
            # logging.warning(data)
            response_data = {
                "blr": endswitch,
                "rt1": 2,
                "rt2": 2,
                "rt3": 2,
                "wifiid": 0,
                "wifipass": 0,
            }
            return Response(response_data, status=200)

        return Response(status=200)

        #     # run optimization check (temp limits controll)

        #     # heating_utility_start = time.time()
        #     heating_optimization_utility(data)
        #     # heating_utility_end = time.time()

        #     # push data to a redis stream
        #     dao.add_ioniq_to_data_stream(data)

        #     # push data to postgres cold database
        #     async_task("devices.utils.insert_ioniqmax_device_data", data)

        #     # push update ping to online statuses redis stream
        #     try:
        #         dao.add_ioniq_to_online_stream(sn)
        #     except Exception as e:
        #         logging.warning(
        #             f"Unable to push online status update to redis stream {e}"
        #         )

        #     device_vars_dict = fetch_device_variables(data["sn"])

        #     # print("optimization func time", heating_utility_end - heating_utility_start, " sec")

        #     return Response(device_vars_dict, status=200)
        # else:
        #     return Response(serializer.error_messages, status=400)


class IoniqMaxSystemStatusApiView(APIView):
    """Ioniq Max mockup API"""

    permission_classes = [AllowAny]

    def post(self, request):
        return Response(status=200)

        # serializer = IoniqMaxSystemStateSerializer(data=request.data)

        # if serializer.is_valid(raise_exception=True):
        #     token = serializer.validated_data.get("token")
        #     if token != THERMOSTAT_TOKEN:
        #         return Response("Invalid token", status=403)
        #     data = {
        #         "sn": serializer.validated_data.get("sn"),
        #         "cpu_temp": serializer.validated_data.get("cpu_temp"),
        #         "signal_level": serializer.validated_data.get("signal_level"),
        #         "codebase_ver": serializer.validated_data.get("codebase_ver"),
        #         "last_reload_dt": serializer.validated_data.get("last_reload_dt"),
        #         "reloads_num": serializer.validated_data.get("reloads_num"),
        #     }
        #     async_task("devices.utils.insert_ioniqmax_system_data", data)
        #     return Response(status=200)
        # else:
        #     return Response(serializer.error_messages, status=400)


class IoniqMaxForceUpgradeApiView(APIView):
    """Takes post request to update devicevariables
    with wifiid wifipass (force upgrade)
    """

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = IoniqMaxUpgradeRequestSerializer(data=request.data)

        if serializer.is_valid():
            token = serializer.validated_data.get("token")
            if token != THERMOSTAT_TOKEN:
                return Response("Invalid token", status=403)

            sn = serializer.validated_data.get("sn")
            status = serializer.validated_data.get("status")

            async_task("devices.utils.force_upgrade_variables", sn, status)

            return Response(status=200)


# IONIQ MINI APIs


class IoniqMiniStatusUpdateApiView(APIView):
    """
    Receives ioniq's s/n and returns "on" if related
    zone thermostats statuses includes at least one
    call for heat status.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        ctx = None

        serializer = IoniqMiniStatusRequestSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            token = serializer.validated_data.get("token")

            if token != THERMOSTAT_TOKEN:
                # ctx['status'] = "Access not authorized. Invalid token."
                return Response(status=403)

            sn = serializer.validated_data.get("sn")

            # Schedule async to task to insert new row to online_status table
            # in IoT database
            async_task("devices.utils.insert_status_update", sn)
            r = dao.add_ioniq_to_online_stream(sn)

            final, errors = calculate_ioniqmini_response(sn)
            # print("Final", final)
            # print("errors", errors)
            if errors:
                return HttpResponse(errors)

            response = None
            if final == True:
                response = "on"
            else:
                response = "off"
            return Response(response, status=200)


class IoniqMinitStatusChangeApiView(APIView):
    """[summary]

    Args:
        APIView ([type]): [description]

    Returns:
        [type]: [description]

    systmp - temperature of controller
    """

    permission_classes = [AllowAny]

    def post(self, request):
        ctx = None

        serializer = IoniqMiniStatusRequestSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            token = serializer.validated_data.get("token")

            if token != THERMOSTAT_TOKEN:
                return Response(status=403)

            sn = serializer.validated_data.get("sn")
            systemp = serializer.validated_data.get("systemp")
            endswitch = serializer.validated_data.get("endswitch")

            async_task("devices.utils.insert_controller_data", sn, systemp, endswitch)
            return Response(status=200)
        else:
            return Response(serializer.error_messages, status=500)


# LEGACY ENDPOINTS


class SetRoomTempOnChange(APIView):
    """
    Allow smart thermostats to post data
    whenever setpoint value changes
    """

    permission_classes = [AllowAny]

    def post(self, request):
        # ctx = {
        #     'status': None,
        #     'settpoint': None,
        # }
        serializer = ThermostatDataSerializser(data=request.data)
        if serializer.is_valid(raise_exception=True):

            token = serializer.validated_data.get("token")

            if token != THERMOSTAT_TOKEN:
                # ctx['status'] = "Access not authorized. Invalid token."
                return Response(status=403)

            sn = serializer.validated_data.get("sn")
            roomtemp = serializer.validated_data.get("roomtemp")
            settpoint = serializer.validated_data.get("settpoint")
            status = serializer.validated_data.get("status")

            payload = {
                "sn": sn,
                "roomtemp": roomtemp,
                "settpoint": settpoint,
                "status": status,
            }

            dao.add_thermostat_to_data_stream(payload=payload)

            async_task(
                "devices.utils.update_thermostat_data_on_change",
                sn,
                roomtemp,
                settpoint,
                status,
            )
            # update_device_variables_smart_max(serial_num: str, status: int)
            async_task("external.utils.update_device_variables_smart_max", sn, status)
            set_temperature = get_thermostat_set_point(sn)

            if set_temperature is not None:
                return Response(int(set_temperature), status=200)

            # ctx['status'] = "Temperature was successfully set"
            # ctx['settpoint'] = settpoint
            return Response(int(settpoint), status=200)


class SetDeviceOnlineStatus(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ctx = {
            "set_temperature": None,
        }
        serializer = DevinceOnlineRequestSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            token = serializer.validated_data.get("token")

            if token != THERMOSTAT_TOKEN:
                # ctx['status'] = "Access not authorized. Invalid token."
                return Response(status=403)

            sn = serializer.validated_data.get("sn")

            # UPDATE STATUS TABLE IN A BACKGROUND TASK
            async_task("devices.utils.insert_status_update", sn)

            # PUSH RECORD TO THE REDIS Stream

            r = dao.add_thermostat_to_online_stream(sn)

            # GRAB LAST SETPOINT COMMAND FROM DJANGO MODEL FIELD (IF not NULL)
            # RETURN IMMEDIATLY TO THE API CLIENT
            set_temperature = get_thermostat_set_point(sn)

            if set_temperature is not None:
                ctx["set_temperature"] = set_temperature
                return Response(ctx, status=200)

            # Grab last record from thermostatdata table
            return Response(ctx, status=200)


class ProcessRelayThermostatDataApiView(APIView):
    """
    Supports custom pair of devices communication flow
    in which ioniq mini and thermostat should receive
    each others state trough redis stream
    """

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = ControllerRelayPairDataSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):

            token = serializer.validated_data.get("token")

            if token != THERMOSTAT_TOKEN:
                return Response("Invalid token", status=403)

            type = serializer.validated_data.get("type")
            sn1 = serializer.validated_data.get("sn1")
            sn2 = serializer.validated_data.get("sn2")

            if type not in ["thermostat", "controller"]:
                detail = "Unexpected device type"
                return Response(detail, status=400)

            if type == "controller":
                payload = dict(serializer.validated_data)
                dao.set_paired_relay_controller_data(sn=sn1, payload=payload)
                thermostat_data = dao.get_paired_thermostat_data(sn=sn2)
                if thermostat_data is None:
                    return Response()

                return Response(
                    {
                        "relay": thermostat_data["relay"],
                        "t1": thermostat_data["t1"],
                        "t2": thermostat_data["t2"],
                    },
                    status=200,
                )

            if type == "thermostat":
                payload = dict(serializer.validated_data)
                dao.set_paired_thermostat_data(sn=sn1, payload=payload)
                # dao.set_thermostat_data_hash(sn=sn1, payload=payload)

                setpoint = dao.get_thermostat_setpoint(sn=sn1)
                controller_data = dao.get_paired_relay_controller_data(sn=sn2)

                if setpoint is None:
                    setpoint = 0

                    # Deprecated [uses signal to set TTL on last setpoint]
                    # try:
                    #     thermostat = SmartThermostatModel.objects.get(serial_num=sn1)
                    #     setpoint = thermostat.set_temperature
                    #     dao.set_thermostat_setpoint(sn=sn1, setpoint=setpoint)
                    # except Exception as exc:
                    #     logging.warning(exc)

                if controller_data is None:
                    return Response({"setpoint": setpoint}, status=200)

                return Response(
                    {
                        "setpoint": setpoint,
                        "t1": controller_data["t1"],
                        "t2": controller_data["t2"],
                    },
                    status=200,
                )
        else:
            return Response("Bad input", status=500)


class ProcessPairedMiniDataApiView(APIView):
    """
    Supports custom device communication flow
    in which pair of ioniq minis should recieved
    each others state trough redis stream
    """

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = ControllerRelayPairDataSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):

            token = serializer.validated_data.get("token")

            if token != THERMOSTAT_TOKEN:
                return Response("Invalid token", status=403)

            sn1 = serializer.validated_data.get("sn1")
            sn2 = serializer.validated_data.get("sn2")

            payload = dict(serializer.validated_data)
            dao.set_paired_relay_controller_data(sn=sn1, payload=payload)
            thermostat_data = dao.get_paired_thermostat_data(sn=sn2)
            try:
                thermostat_t1 = thermostat_data["t1"]
                thermostat_relay = thermostat_data["relay"]
                thermostat_setpoint = thermostat_data["setpoint"]
            except Exception as exc:
                logging.warning(exc)
                thermostat_t1 = None
                thermostat_relay = None
                thermostat_setpoint = None

            return Response(
                {
                    "relay": thermostat_relay,
                    "t1": thermostat_t1,
                    "setpoint": thermostat_setpoint,
                },
                status=200,
            )


class ProcessPairedThermostatDataApiView(APIView):
    """
    Supports custom device communication flow
    in which pair of ioniq minis should recieved
    each others state trough redis stream
    """

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = ControllerRelayPairDataSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):

            token = serializer.validated_data.get("token")

            if token != THERMOSTAT_TOKEN:
                return Response("Invalid token", status=403)

            sn1 = serializer.validated_data.get("sn1")
            sn2 = serializer.validated_data.get("sn2")

            payload = dict(serializer.validated_data)
            dao.set_paired_thermostat_data(sn=sn1, payload=payload)
            # dao.set_thermostat_data_hash(sn=sn1, payload=payload)
            controller_data = dao.get_paired_relay_controller_data(sn=sn2)

            try:
                controller_t1 = controller_data["t1"]
                controller_t2 = controller_data["t2"]
                controller_relay = controller_data["relay"]
            except Exception as exc:
                logging.warning(exc)
                controller_t1 = None
                controller_t2 = None
                controller_relay = None

            setpoint = dao.get_thermostat_setpoint(sn=sn1)

            if setpoint is None:
                try:
                    thermostat = SmartThermostatModel.objects.get(serial_num=sn1)
                    setpoint = thermostat.set_temperature
                    dao.set_thermostat_setpoint(sn=sn1, setpoint=setpoint)
                except:
                    setpoint = "-100"
            custom_setpoint = setpoint
            return Response(
                {
                    "setpoint": custom_setpoint,
                    "t1": controller_t1,
                    "t2": controller_t2,
                    "relay": controller_relay,
                },
                status=200,
            )


class ServiceThermostatDataRetrieveApiView(APIView):
    """
    Allow service access to thermostat data inside
    redis stream
    """
    authentication_classes = [ServiceTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        serial_num = self.kwargs.get("serial_num")

        thermostat_data = dao.get_paired_thermostat_data(sn=serial_num)
        if thermostat_data is not None:
            thermostat_data.pop("token", None)

        return Response(data=thermostat_data, status=200)


class ServiceControllerDataRetrieveApiView(APIView):
    """
    Allow service access to controller data inside
    redis stream
    """
    authentication_classes = [ServiceTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):

        serial_num = self.kwargs.get("serial_num")

        controller_data = dao.get_paired_relay_controller_data(sn=serial_num)

        if controller_data is None:
            return Response(data={"detail": "No data"}, status=400)

        controller_data.pop("token", None)

        boiler_data = dao.get_boiler_data(sn=serial_num)

        if boiler_data is not None:
            logger.info("Redis info on boiler {} controller {}", boiler_data, serial_num)
            controller_data["boiler_type"] = boiler_data.get("boiler_type", None)
            controller_data["wwsd"] = boiler_data.get("wwsd", 0)
            logger.info("boiler type A {}", controller_data["boiler_type"])
        else:
            try:
                controller = IoniqControllerModel.objects.select_related('boiler').get(serial_num=serial_num)
            except IoniqControllerModel.DoesNotExist:
                return Response(data={"detail": "Controller is not configured"}, status=400)
            wwsd = 0
            if controller.boiler:
                boiler_data = controller.boiler
                controller_data["wwsd"] = 1 if boiler_data.shutdown_active else 0
                controller_data["boiler_type"] = boiler_data.type
                logger.info("boiler type B {}", controller_data["boiler_type"])
                dao.set_boiler_data(sn=serial_num, payload={"type": boiler_data.type, "wwsd": wwsd})

        return Response(data=controller_data, status=200)
