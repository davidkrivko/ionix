from django_q.tasks import async_task
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from devices.models import SmartThermostatModel
from .models import (
    DeviceScheduleModel,
    ThermostatSubscriberModel,
    HeatSwitchSubscriberModel,
    AnalogueThermostatSubscriberModel, ZoneSubscriberModel,
)
from .serializers import (
    ScheduleOptionsModelSerializer,
    ThermostatSubscriberModelSerializer,
    ThermostatSubscriberModelCreateSerializer,
    SwitchSubscriberModelSerializer,
    SwitchSubscriberModelCreateSerializer,
    AnalogueSubscriberModelCreateSerializer,
    AnalogueSubscriberModelSerializer,
    ModelPkSerializer, ZoneSubscriberModelSerializer,
)


class ScheduleChoicesListView(ListAPIView):
    """
    List all options with id for the
    weekday specified
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ScheduleOptionsModelSerializer

    def get_queryset(self):

        weekday_id = self.kwargs.get("weekday")  # int

        if weekday_id is None:
            return None

        queryset = DeviceScheduleModel.objects.filter(week_day=weekday_id)

        if not queryset.exists():
            return DeviceScheduleModel.objects.none()

        return queryset


# class LandlordOffHoursSettingsListView(ListAPIView):
#     """Allow landlords to list new off-hours
#     range settings
#     """
#     serializer_class = LandlordOffHoursScheduleModelSerializer


#     def get_queryset(self):

#         boiler_id = self.kwargs.get("boiler_id")
#         try:
#             queryset = LandlordOffHoursScheduleModel.objects.filter(owner = self.request.user.owner, boiler__pk=boiler_id)
#         except:
#             queryset = LandlordOffHoursScheduleModel.objects.none()
#         return queryset


# class LandlordOffHoursSettingsCreateView(CreateAPIView):
#     """Allow landlords to create new off-hours
#     range settings
#     """
#     serializer_class = LandlordOffHoursScheduleModelSerializer

#     def get_queryset(self):
#         try:
#             queryset = LandlordOffHoursScheduleModel.objects.all()
#         except:
#             queryset = LandlordOffHoursScheduleModel.objects.none()

#         return queryset

#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user.owner)


# class LandlordOffHoursSettingsDeleteView(APIView):
#     """
#     Removes off-hours schedule record
#     """
#     def post(self, request):

#         serializer = ModelPkSerializer(data=request.data)
#         if serializer.is_valid():
#             pk = serializer.validated_data.get('pk')
#             try:
#                 obj = LandlordOffHoursScheduleModel.objects.get(pk=pk, owner = request.user.owner)
#             except:
#                 return Response(status=404)
#             obj.delete()
#             return Response(status=204)


# SMART THERMOSTATS BLOCK

class ScheduleSubscriberApiView(ListAPIView):
    """
    Allow property owners to list schedule events for their
    smart thermostats
    """
    serializer_class = ThermostatSubscriberModelSerializer

    def get_queryset(self):

        thermostat_id = self.request.GET.get("device_id")
        if thermostat_id is not None:
            queryset = ThermostatSubscriberModel.objects.filter(
                thermostat__id=thermostat_id,
                owner=self.request.user.owner
            )  # .order_by('schedule__week_day')
        else:
            queryset = ThermostatSubscriberModel.objects.filter(owner=self.request.user.owner)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.owner)


class ScheduleSubscriberCreateApiView(CreateAPIView):
    """
    Allow property owners to create schedule events for their
    smart thermostats
    """
    serializer_class = ThermostatSubscriberModelCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.owner)

    def get_queryset(self):
        queryset = ThermostatSubscriberModel.objects.all()
        return queryset


class ScheduleSubscriberDeleteApiView(APIView):
    """
    Removes ThermostatSubscriber object
    """

    def post(self, request):

        serializer = ModelPkSerializer(data=request.data)
        if serializer.is_valid():
            pk = serializer.validated_data.get('pk')
            try:
                obj = ThermostatSubscriberModel.objects.get(pk=pk, owner=request.user.owner)
            except:
                return Response(status=404)
            obj.delete()
            return Response(status=204)


# SIMPLE HEATSWITCHES BLOCK

class ScheduleSwitchSubscriberApiView(ListAPIView):
    """
    Allow property owners to list schedule events for their
    heat switches
    """
    serializer_class = SwitchSubscriberModelSerializer

    def get_queryset(self):

        switch_id = self.request.GET.get("device_id")
        if switch_id is not None:
            queryset = HeatSwitchSubscriberModel.objects.filter(switch__id=switch_id,
                                                                owner=self.request.user.owner)  # .order_by('schedule__week_day')
        else:
            queryset = HeatSwitchSubscriberModel.objects.filter(owner=self.request.user.owner)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.owner)


class SchedulSwitcheSubscriberCreateApiView(CreateAPIView):
    """
    Allow property owners to create schedule events for their
    heat switches
    """
    serializer_class = SwitchSubscriberModelCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.owner)

    def get_queryset(self):
        queryset = HeatSwitchSubscriberModel.objects.filter(owner=self.request.user.owner)
        return queryset


class ScheduleSwitchSubscriberDeleteApiView(APIView):
    """
    Removes SimpleSwitchSubscriber object
    """

    def post(self, request):
        serializer = ModelPkSerializer(data=request.data)
        if serializer.is_valid():
            pk = serializer.validated_data.get('pk')
            try:
                obj = HeatSwitchSubscriberModel.objects.get(pk=pk, owner=request.user.owner)
            except:
                return Response(status=404)
            obj.delete()
            return Response(status=204)


# ANALOGUE THERMOSTATS BLOCK

class ScheduleAnalogueSubscriberApiView(ListAPIView):
    """
    Allow property owners to list schedule events for their
    analogue thermostats
    """
    serializer_class = AnalogueSubscriberModelSerializer

    def get_queryset(self):

        thermostat_id = self.request.GET.get("device_id")
        if thermostat_id is not None:
            queryset = AnalogueThermostatSubscriberModel.objects.filter(analogue_thermostat__id=thermostat_id,
                                                                        owner=self.request.user.owner)  # .order_by('schedule__week_day')
        else:
            queryset = AnalogueThermostatSubscriberModel.objects.filter(owner=self.request.user.owner)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.owner)


class ScheduleAnalogueSubscriberCreateApiView(CreateAPIView):
    """
    Allow property owners to create schedule events for their
    analogue thermostats
    """
    serializer_class = AnalogueSubscriberModelCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.owner)

    def get_queryset(self):
        queryset = AnalogueThermostatSubscriberModel.objects.filter(owner=self.request.user.owner)
        return queryset


class ScheduleAnalogueSubscriberDeleteApiView(APIView):
    """
    Removes AnalogueThermostatSubscriber object
    """

    def post(self, request):

        serializer = ModelPkSerializer(data=request.data)
        if serializer.is_valid():
            pk = serializer.validated_data.get('pk')
            try:
                obj = AnalogueThermostatSubscriberModel.objects.get(pk=pk, owner=request.user.owner)
            except:
                return Response(status=404)
            obj.delete()
            return Response(status=204)


# TENANTS SCHEDULE FLOW

# SMART THERMOSTATS BLOCK

class TenantScheduleSubscriberApiView(ListAPIView):
    """
    Allow property owners to list schedule events for their
    smart thermostats
    """
    serializer_class = ThermostatSubscriberModelSerializer

    def get_queryset(self):

        thermostat_id = self.request.GET.get("device_id")
        if thermostat_id is not None:
            queryset = ThermostatSubscriberModel.objects.filter(thermostat__id=thermostat_id,
                                                                owner=self.request.user.tenant.owner)  # .order_by('schedule__week_day')
        else:
            queryset = ThermostatSubscriberModel.objects.filter(owner=self.request.user.tenant.owner)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.owner)


class TenantScheduleSubscriberCreateApiView(CreateAPIView):
    """
    Allow property owners to create schedule events for their
    smart thermostats
    """
    serializer_class = ThermostatSubscriberModelCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.tenant.owner)

    def get_queryset(self):
        queryset = ThermostatSubscriberModel.objects.all()
        return queryset


class TenantScheduleSubscriberDeleteApiView(APIView):
    """
    Removes ThermostatSubscriber object
    """

    def post(self, request):

        serializer = ModelPkSerializer(data=request.data)
        if serializer.is_valid():
            pk = serializer.validated_data.get('pk')
            try:
                obj = ThermostatSubscriberModel.objects.get(pk=pk, owner=request.user.tenant.owner)
            except:
                return Response(status=404)
            obj.delete()
            return Response(status=204)


# HEATING ZONE BLOCK


class ZoneSubscriberViewSet(viewsets.ModelViewSet):
    serializer_class = ZoneSubscriberModelSerializer

    def get_queryset(self):
        queryset = ZoneSubscriberModel.objects.filter(owner=self.request.user.owner)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            zone_id = serializer.validated_data.get("heating_zone")
            thermostats = SmartThermostatModel.objects.filter(
                zone=zone_id
            ).select_related("zone")
            for therm in thermostats:
                ThermostatSubscriberModel.objects.create(
                    setpoint=serializer.validated_data.get("setpoint"),
                    schedule=serializer.validated_data.get("schedule"),
                    thermostat=therm,
                    owner=serializer.validated_data.get("owner")
                )
            super(ZoneSubscriberViewSet, self).create(request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_404_NOT_FOUND)
