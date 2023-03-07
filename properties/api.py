from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ChangePropertyNameSerializer
from .models import (
    RoomModel,
    ApartmentModel,
    ZoneModel
)
from django.utils import timezone

now = timezone.now


class CheckLastTemperatureApiView(APIView):
    """Allow tenants to parse last temperature
    observation from Zip code model field
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ctx = {
            "detail": None,
            "data": {
                "temp_f": None,
            },
        }
        zip_code = None
        # allow parsing by building id for landlords
        build_id = request.GET.get('build_id')
        try:
            owner = request.user.owner
        except:
            owner = None
        if build_id is not None and owner is not None:
            zip_code = owner.buildings.get(pk=build_id).zip_code
        elif owner is not None:
            zip_code = owner.buildings.last().zip_code
        else:
            zip_code = request.user.tenant.rooms.last().apartment.building.zip_code

        if zip_code is not None:
            if zip_code.updated_at.date() == now().date() and zip_code.todays_temp is not None:
                ctx['data']['temp_f'] = zip_code.todays_temp

        return Response(ctx, status=200)


class ChangeZoneNameApiView(APIView):
    """
    3Allow owners to change zone names
    """
    def post(self, request):

        ctx = {
            'detail': None,
            'data': None,
        }

        serializer = ChangePropertyNameSerializer(data=request.data)

        if serializer.is_valid():
            id = serializer.validated_data.get('id')
            name = serializer.validated_data.get('name')

            try:
                zone = ZoneModel.objects.get(pk=id)
            except:
                return Response(status=404)

            zone.name = name
            zone.save()

            ctx['detail'] = "Zone name was successfully updated"
            ctx['data'] = {"name": name}
            return Response(ctx, status=200)
            

class ChangeRoomNameApiView(APIView):
    """
    Allow Tenants and owners change room names
    """
    def post(self, request):

        ctx = {
            'detail': None,
            'data': None,
        }

        serializer = ChangePropertyNameSerializer(data=request.data)

        if serializer.is_valid():
            id = serializer.validated_data.get('id')
            name = serializer.validated_data.get('name')

            try:
                room = RoomModel.objects.get(pk=id)
            except:
                return Response(status=404)

            room.name = name
            room.save()

            ctx['detail'] = "Room name was successfully updated"
            ctx['data'] = {"name": name}

            return Response(ctx, status=200)


class FetchUpdateRoomNameApiView(APIView):
    """
    Allow Tenants and owners change room names
    """
    def get(self, request):
        ctx = {
            'detail': None,
            'data': None,
        }
        apart_id = request.GET.get("apart_id")

        try:
            apartment = ApartmentModel.objects.get(pk=apart_id)
        except:
            return Response(status=404)

        ctx['data'] = apartment.name
        return Response(ctx, status=200)


    def post(self, request):
        ctx = {
            'detail': None,
            'data': None,
        }
        serializer = ChangePropertyNameSerializer(data=request.data)

        if serializer.is_valid():
            id = serializer.validated_data.get('id')
            name = serializer.validated_data.get('name')
            try:
                apartment = ApartmentModel.objects.get(pk=id)
            except:
                return Response(status=404)

            apartment.name = name
            apartment.save()

            ctx['detail'] = "Apartment name was successfully updated"
            ctx['data'] = {"name": name}

            return Response(ctx, status=200)
