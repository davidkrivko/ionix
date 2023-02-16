from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from users.models import TenantProfileModel
from properties.models import RoomModel
from properties.serializers import RoomModelSerializer
from django.db.models import Count


class RoomsListApiView(ListAPIView):
    """Allow tenant users request
    their rooms and thermostats data
    """

    serializer_class = RoomModelSerializer

    def get_queryset(self):

        try:
            tenant = self.request.user.tenant
        except:
            return RoomModel.objects.none()

        queryset = tenant.rooms.all().annotate(
            smart_thermostats_count=Count('thermostat'), 
            heat_switch_count=Count('heat_switch'),
            analogue_thermostats_count=Count('analogue_thermostat')
            )

        return queryset




class GetBoilerIdApiView(APIView):
    """Allow tenants to parse boiler id
    for further wwsd data request"""

    def get(self, request):
        tenant = None
        try:
            tenant = self.request.user.tenant
        except:
            return Response(status=404)
        boiler_id = None

        try:
            boiler_id = tenant.rooms.first().apartment.boiler.pk
        except:
            try:
                boiler_id = tenant.rooms.first().apartment.building.boiler.pk
            except:
                return Response(status=404)

        if boiler_id is not None:
            return Response(boiler_id, status=200)
        else:
            return Response(status=404)
