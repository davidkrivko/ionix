from rest_framework import serializers


class IoniqMiniStatusRequestSerializer(serializers.Serializer):

    token = serializers.CharField()
    sn = serializers.CharField()
    systemp = serializers.IntegerField(required=False)
    endswitch = serializers.IntegerField(required=False)


class IoniqMaxDataSerializer(serializers.Serializer):

    token = serializers.CharField()
    sn = serializers.CharField()
    icsmain = serializers.DecimalField(decimal_places=2, max_digits=5)
    ics1 = serializers.DecimalField(decimal_places=2, max_digits=5)
    ics2 = serializers.DecimalField(decimal_places=2, max_digits=5)
    ics3 = serializers.DecimalField(decimal_places=2, max_digits=5)
    icsboiler = serializers.DecimalField(decimal_places=2, max_digits=5)
    t1 = serializers.IntegerField()
    t2 = serializers.IntegerField()
    t3 = serializers.IntegerField()
    t4 = serializers.IntegerField()
    t5 = serializers.IntegerField()
    t6 = serializers.IntegerField()
    t7 = serializers.IntegerField()
    t8 = serializers.IntegerField()
    rt1 = serializers.IntegerField()
    rt2 = serializers.IntegerField()
    rt3 = serializers.IntegerField()
    endswitch = serializers.IntegerField()
    ps = serializers.DecimalField(decimal_places=2, max_digits=5)


class IoniqMaxSystemStateSerializer(serializers.Serializer):

    token = serializers.CharField()
    sn = serializers.CharField()
    signal_level = serializers.IntegerField()
    cpu_temp = serializers.IntegerField()
    codebase_ver = serializers.CharField()
    last_reload_dt = serializers.DateTimeField()
    reloads_num = serializers.IntegerField()


class IoniqMaxUpgradeRequestSerializer(serializers.Serializer):

    token = serializers.CharField()
    sn = serializers.CharField()
    status = serializers.BooleanField()


class ControllerRelayPairDataSerializer(serializers.Serializer):

    token = serializers.CharField()
    type = serializers.CharField(required=False)
    sn1 = serializers.CharField()
    sn2 = serializers.CharField()
    t1 = serializers.IntegerField()
    t2 = serializers.IntegerField(required=False)
    setpoint = serializers.IntegerField(required=False)
    relay = serializers.IntegerField(required=False)
    sw_ver = serializers.CharField(required=False)
    rssi = serializers.IntegerField(required=False)
    cpu_t = serializers.IntegerField(required=False)
    ap_users = serializers.IntegerField(required=False)
    local_ip = serializers.CharField(required=False)
