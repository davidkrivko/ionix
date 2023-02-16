from django_filters import rest_framework as filters
from .models import ApartmentModel, BuildingModel


class BuidlingModelFilter(filters.FilterSet):

    class Meta:
        model = BuildingModel
        fields = ['name', 'address']

    name = filters.CharFilter(lookup_expr='icontains')
    address = filters.CharFilter(lookup_expr='icontains')


class ApartmentModelFilter(filters.FilterSet):

    class Meta:
        model = ApartmentModel
        fields = ['leaseholder', 'is_alert', 'is_vacant']
   
    leaseholder = filters.CharFilter(field_name="leaseholder", lookup_expr='icontains')
    building = filters.CharFilter(field_name="building__address", lookup_expr='icontains')

    is_alert = filters.BooleanFilter()
    is_vacant = filters.BooleanFilter()
