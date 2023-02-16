from django.contrib import admin
from .models import (
    IoniqControllerModel,
    SmartThermostatModel,
    AnalogueThermostatModel,
    SensorModel,
    BoilerModel,
    SimpleSwitchModel,
)
# Register your models here.

admin.site.register(IoniqControllerModel)
admin.site.register(SmartThermostatModel)
admin.site.register(AnalogueThermostatModel)
admin.site.register(SimpleSwitchModel)
admin.site.register(SensorModel)
admin.site.register(BoilerModel)