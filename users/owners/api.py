from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from users.models import TenantProfileModel
from properties.models import (
    ApartmentModel, 
    BuildingModel, 
    RoomModel
)
from properties.serializers import (
    RoomModelSerializer, 
    ApartmentModelSerializer,
    BuildingModelSerializer,
    ApartmentThermostatLimitsSerializer,
)
# from django.db.models import Count
from users.serializers import (
    TenantModelSerializer,
    UserIdSerializer,
)
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from users.tokens import user_tokenizer
from django.conf import settings

from django_q.tasks import async_task
from django.urls import reverse
from django.db.models import F
from django_filters import rest_framework as filters
from properties.filters import ApartmentModelFilter, BuidlingModelFilter

CURRENT_SITE = settings.CURRENT_SITE
User = get_user_model()


class BuildingListApiView(ListAPIView):
    """Allow landlord owners to list
    their building/properties
    """
    serializer_class = BuildingModelSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BuidlingModelFilter
    
    def get_queryset(self):

        try:
            owner = self.request.user.owner
        except:
            return BuildingModel.objects.none()
        
        queryset = BuildingModel.objects.filter(owner=owner).order_by('address')

        return queryset


class ApartmentsListApiView(ListAPIView):
    """Allow owners to request
    their apartments list
    """

    serializer_class = ApartmentModelSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ApartmentModelFilter

    def get_queryset(self):
        # filter by building id if present
        build_id = self.request.GET.get('build_id')
        try:
            owner = self.request.user.owner
        except:
            return ApartmentModel.objects.none()
        
        if build_id is not None:
            queryset = ApartmentModel.objects.filter(building__owner=owner, building__pk=build_id)\
                .annotate(controller_sn=F('boiler__ioniq_controller__serial_num'), controller_type=F('boiler__ioniq_controller__model_type')).order_by('name')
        else:
            queryset = ApartmentModel.objects.filter(building__owner=owner)\
                .annotate(controller_sn=F('boiler__ioniq_controller__serial_num'), controller_type=F('boiler__ioniq_controller__model_type')).order_by('name')

        return queryset

    
class ApartmentThermostatRangeApiView(APIView):
    """Allow owners and landlords to change
    thermostat range limits for their tenants
    """
    def post(self, request):
        ctx = {
            'detail': None,
            'data': None,
        }
        serializer = ApartmentThermostatLimitsSerializer(data=request.data)
        if serializer.is_valid():
            id = serializer.validated_data.get("id")
            min_temp = serializer.validated_data.get("min_temp")
            max_temp = serializer.validated_data.get("max_temp")
            tlimits_is_on = serializer.validated_data.get("tlimits_is_on")
            try:
                apartment = ApartmentModel.objects.get(id=id, building__owner=request.user.owner)
            except:
                return Response(status=404)
           
            apartment.min_temp = min_temp
            apartment.max_temp = max_temp
            apartment.tlimits_is_on = tlimits_is_on
            apartment.save()
            ctx['detail'] = "Thermostat limits were successfully set"
            return Response(ctx, status=200)
        else:
            return Response(serializer.error_messages, status=400)


class RetrieveRoomsAPIView(ListAPIView):
    """Allow owner users request
    their rooms and thermostats data
    """
    permission_classes = [IsAuthenticated]
    serializer_class = RoomModelSerializer

    def get_queryset(self):

        apart_id = self.kwargs.get('id')

        try:
            apartment = ApartmentModel.objects.get(pk=apart_id)
        except:
            apartment = ApartmentModel.objects.none()
    
        try:
            rooms = apartment.rooms.order_by('name')
        except:
            rooms = RoomModel.objects.none()

        return rooms



class OwnerRoomsListApiView(ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = RoomModelSerializer

    def get_queryset(self):
        try:
            owner = self.request.user.owner
            queryset = RoomModel.objects.filter(apartment__building__owner=owner).order_by('name')
        except:
            queryset = RoomModel.objects.none()
        return queryset
            

        
class OwnersTenantsApiListView(ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = TenantModelSerializer

    def get_queryset(self):

        #Query params
        guests = self.request.GET.get('guests')
        apartment_id = self.request.GET.get('apartment_id')
        
        try:
            tenants = self.request.user.owner.tenants
            tenants_queryset = tenants 
        except:
            tenants = None
            tenants_queryset = TenantProfileModel.objects.none()

        if apartment_id is not None:
            try:
                apartment = ApartmentModel.objects.get(pk=apartment_id)
                room_ids = apartment.rooms.values_list('id', flat=True)
                tenants_queryset = tenants.filter(rooms__in=room_ids)
            except:
                return TenantProfileModel.objects.none()


        if guests=='true':
            queryset = tenants_queryset.filter(is_guest=True).annotate(email=F('user__username')).distinct()
        else:
            queryset = tenants_queryset.filter(is_guest=False).annotate(email=F('user__username')).distinct()
        return queryset


    def perform_create(self, serializer):
        # NB Add check if is_guest creation/ otherwise use custom email
        string = get_random_string(length=5)
        password = get_random_string(length=6)

        email = serializer.validated_data.get("email")
        if email is not None:
            username = email
        else:
            username = f"tenant_{string}@turnonheat.com"
        user = User(username=username)
        user.set_password(password)
        user.save()

        token = user_tokenizer.make_token(user)
        user_id = urlsafe_base64_encode(force_bytes(user.pk))
        url = CURRENT_SITE + reverse('guest-page', kwargs={'user_id': user_id, 'token': token})
        serializer.save(owner=self.request.user.owner, user=user, access_link=url)



class DeleteTenantApiView(APIView):
    """Allow owners to delete their tenants
    """
    permission_classes = [IsAuthenticated]
    serializer_class = TenantModelSerializer

    def post(self, request):
        ctx = {
            "detail": None
        }
        serializer = UserIdSerializer(data=request.data)

        if serializer.is_valid():
            id = serializer.validated_data.get("id")

            try:
                tenant = TenantProfileModel.objects.get(pk=id)
            except:
                return Response(status=404)
            
            if request.user.owner != tenant.owner:
                return Response(status=403)

            
            user = tenant.user
            user.delete()
            ctx['detail'] = "Your tenant was successfully removed"

            return Response(ctx, status=200)


class RequestPasswordResetLinkApiView(APIView):
    """[summary]

    Args:
        APIView ([type]): [description]
    """

    def post(self, request):
        ctx = {
            "detail": None
        }
        serializer = UserIdSerializer(data=request.data)

        if serializer.is_valid():
            id = serializer.validated_data.get("id")
            email = serializer.validated_data.get("email")

            try:
                tenant = TenantProfileModel.objects.get(pk=id)
            except:
                return Response(status=404)
            
            if request.user.owner != tenant.owner:
                return Response(status=403)

            ctx['detail'] = "Password reset link was successfully sent"

            async_task("users.utils.send_tenant_password_reset_link", id, email)

            return Response(ctx, status=200)



class SetTenantAsLeaseHolderAPiView(APIView):
    """Allow landlord to set tenant as a leaseholder
    Uses tenant name to fill in / overwrite respective 
    field on Apartment model
    """

    def post(self, request):
        ctx = {
            "detail": None
        }
        serializer = UserIdSerializer(data=request.data)

        if serializer.is_valid():
            id = serializer.validated_data.get("id")

            try:
                tenant = TenantProfileModel.objects.get(pk=id)
            except:
                return Response(status=404)
            
            if request.user.owner != tenant.owner:
                return Response(status=403)

            apartment = tenant.rooms.first().apartment
            apartment.leaseholder = tenant.first_name
            apartment.save()

            return Response(ctx, status=200)


   
class VacantApartmentActionApiView(APIView):
    """Allow property owner to change apartment
    state to vacant and detach/remove all tenants
    at once.
    """

    def post(self, request):

        serializer = UserIdSerializer(data=request.data) #noqa use only id field
        if serializer.is_valid():
            apartment_id = serializer.validated_data.get('id')
            try:
                apartment = ApartmentModel.objects.get(pk=apartment_id)
            except:
                return Response(status=404)
            
            if apartment.building.owner != request.user.owner:
                return Response(status=403)

            apartment.is_vacant = True
            apartment.leaseholder = ''
            apartment.save()
            async_task('workers.tasks.process_vacant_apartment', apartment_id)
            return Response(status=200)
        else:
            return Response(serializer.error_messages, status=500)
