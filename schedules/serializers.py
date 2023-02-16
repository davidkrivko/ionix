from django_q.tasks import schedule
from rest_framework import serializers
from .models import(
    DeviceScheduleModel, 
    ThermostatSubscriberModel,
    HeatSwitchSubscriberModel,
    AnalogueThermostatSubscriberModel,
)
from devices.models import SmartThermostatModel


class ScheduleOptionsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceScheduleModel
        fields = '__all__'
        
# class LandlordOffHoursScheduleModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LandlordOffHoursScheduleModel
#         fields = '__all__'

class ThermostatSubscriberModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = ThermostatSubscriberModel
        exclude = ['created_at', 'updated_at']
        depth = 1

class ThermostatSubscriberModelCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ThermostatSubscriberModel
        exclude = ['created_at', 'updated_at']


class SwitchSubscriberModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = HeatSwitchSubscriberModel
        exclude = ['created_at', 'updated_at']
        depth = 1


class SwitchSubscriberModelCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = HeatSwitchSubscriberModel
        exclude = ['created_at', 'updated_at']

class AnalogueSubscriberModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnalogueThermostatSubscriberModel
        exclude = ['created_at', 'updated_at']
        depth = 1


class AnalogueSubscriberModelCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnalogueThermostatSubscriberModel
        exclude = ['created_at', 'updated_at']




class ModelPkSerializer(serializers.Serializer):
    pk = serializers.IntegerField()