from rest_framework import serializers

from devices.models import (
    BoilerModel,
    IoniqControllerModel,
    SmartThermostatModel,
)


class ControllerModelSerializer(serializers.ModelSerializer):

    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = IoniqControllerModel
        fields = "__all__"


class SmartThermostatModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartThermostatModel
        # fields = "__all__"
        exclude = ["owner"]
        depth = 1


class ThermostatDataSerializser(serializers.Serializer):

    token = serializers.CharField()
    sn = serializers.CharField()
    roomtemp = serializers.CharField()
    settpoint = serializers.CharField()
    status = serializers.CharField(max_length=1)


class DevinceOnlineRequestSerializer(ThermostatDataSerializser):

    roomtemp = None
    settpoint = None
    status = None


class SetTempCommandSerializer(serializers.Serializer):

    thermostat_sn = serializers.CharField()
    set_temperature = serializers.IntegerField()
    status = serializers.BooleanField(required=False)


class DeviceStatusSerializer(serializers.Serializer):

    sn = serializers.CharField()
    device_type = serializers.CharField(required=False)


class HeatSwitchStatusSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    status = serializers.BooleanField()


class BoilerShutDownTempSerializer(serializers.Serializer):

    boiler_id = serializers.IntegerField()
    shutdown_temp = serializers.IntegerField()
    shutdown_enabled = serializers.BooleanField()


class BoilerModelSerializer(serializers.ModelSerializer):

    building_name = serializers.CharField(read_only=True, required=False)
    apartment = serializers.IntegerField(read_only=True, required=False)
    # building = serializers.CharField(read_only=True, required=False)

    class Meta:
        model = BoilerModel
        fields = "__all__"


class DeviceIdSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class NameFieldSerializer(serializers.Serializer):
    name = serializers.CharField()
