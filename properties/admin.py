from django.contrib import admin
from .models import (
    ZipCodeModel,
    ZoneModel,
    BuildingModel,
    ApartmentModel,
    RoomModel,
    ApartmentAlertDetailsModel,
    WeatherRecordModel,
)



admin.site.register(ZipCodeModel)
admin.site.register(BuildingModel)
admin.site.register(ApartmentModel)
admin.site.register(RoomModel)
admin.site.register(ApartmentAlertDetailsModel)
admin.site.register(ZoneModel)
admin.site.register(WeatherRecordModel)