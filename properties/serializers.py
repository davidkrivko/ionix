from rest_framework import serializers
from .models import (
    RoomModel, 
    ApartmentModel,
    BuildingModel,
)



class BuildingModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = BuildingModel
        exclude = ['created_at', 'updated_at']
        

class ApartmentModelSerializer(serializers.ModelSerializer):

    controller_sn = serializers.CharField(read_only=True, required=False)
    controller_type = serializers.CharField(read_only=True, required=False)

    class Meta:
        model = ApartmentModel
        exclude = ['created_at', 'updated_at']
        depth = 1


class RoomModelSerializer(serializers.ModelSerializer):

    smart_thermostats_count=serializers.IntegerField(required=False)
    heat_switch_count=serializers.IntegerField(required=False)
    analogue_thermostats_count=serializers.IntegerField(required=False)
    room_type = serializers.CharField(source='get_room_type_display', read_only=True, required=False)

    class Meta:
        model = RoomModel
        exclude = ['created_at', 'updated_at']
        depth = 1


class ChangePropertyNameSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(required=False)



class ApartmentThermostatLimitsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    max_temp = serializers.IntegerField()
    min_temp = serializers.IntegerField()
    tlimits_is_on = serializers.BooleanField()