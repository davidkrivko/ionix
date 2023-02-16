from django.contrib import admin
from .models import (
    DeviceScheduleModel, 
    ThermostatSubscriberModel,
    HeatSwitchSubscriberModel,
    AnalogueThermostatSubscriberModel,
)
# Register your models here.
admin.site.register(DeviceScheduleModel)
admin.site.register(ThermostatSubscriberModel)
admin.site.register(AnalogueThermostatSubscriberModel)
admin.site.register(HeatSwitchSubscriberModel)