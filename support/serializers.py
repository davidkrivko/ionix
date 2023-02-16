from rest_framework import serializers
from .models import SupportRequestModel



class SuportRequestModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupportRequestModel
        fields = '__all__'