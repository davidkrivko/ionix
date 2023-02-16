from rest_framework import serializers




class HeatingDataDateRangeSerializer(serializers.Serializer):

    sn = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()