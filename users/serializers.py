from rest_framework import serializers
from properties.models import RoomModel
from .models import TenantProfileModel


class NameSerializer(serializers.Serializer):

    first_name = serializers.CharField(max_length=60)
    email = serializers.EmailField(required=False)


class UserIdSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    email = serializers.EmailField(required=False)

class PasswordUpdateSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=False)
    new_password = serializers.CharField()


class TenantModelSerializer(serializers.ModelSerializer):

    rooms_ids = serializers.PrimaryKeyRelatedField(many=True, write_only=True, queryset=RoomModel.objects.all())
    email = serializers.EmailField(required=False)

    class Meta:
        model = TenantProfileModel
        fields='__all__'

    def create(self, validated_data):
        
        # email = validated_data.pop("email", None)
        rooms = validated_data.pop("rooms_ids", None)
        try:
            validated_data.pop("email")
        except:
            pass
        
        tenant = TenantProfileModel.objects.create(**validated_data)

        if rooms:
            tenant.rooms.set(rooms)

        return tenant