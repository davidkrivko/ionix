from django.urls import path
from .api import (
    ProfileDataApiView,
    UpdateTenantPasswordApiView,
    UpdateTenantNameApiView,
    UpdateOwnerProfileApiView,
)
from .owners.api import (
    BuildingListApiView,
    ApartmentsListApiView,
    RetrieveRoomsAPIView,
    OwnersTenantsApiListView,
    OwnerRoomsListApiView,
    DeleteTenantApiView,
    RequestPasswordResetLinkApiView,
    ApartmentThermostatRangeApiView,
    SetTenantAsLeaseHolderAPiView,
    VacantApartmentActionApiView,
)
from .tenants.api import (
    RoomsListApiView,
    GetBoilerIdApiView,
)

urlpatterns = [
    path('me/', ProfileDataApiView.as_view()),
    path('tenant/rooms/', RoomsListApiView.as_view()),
    path('tenant/getboilerid/', GetBoilerIdApiView.as_view()),
    
    path('owner/building/', BuildingListApiView.as_view()),
    path('owner/apartments/', ApartmentsListApiView.as_view()),
    path('owner/apartment/limits/', ApartmentThermostatRangeApiView.as_view()),

    path('owner/rooms/all/', OwnerRoomsListApiView.as_view()),
    path('owner/apartment/<int:id>/', RetrieveRoomsAPIView.as_view()),
    path('owner/apartment/vacant/', VacantApartmentActionApiView.as_view()),
    path('owner/tenants/', OwnersTenantsApiListView.as_view()),
    path('owner/tenant/delete/', DeleteTenantApiView.as_view()),
    path('owner/tenant/reset/', RequestPasswordResetLinkApiView.as_view()),
    path('owner/tenant/leaseholder/', SetTenantAsLeaseHolderAPiView.as_view()),

    path('owner/profile/update/', UpdateOwnerProfileApiView.as_view()),

    path('password/update/', UpdateTenantPasswordApiView.as_view()),
    path('tenant/profile/update/', UpdateTenantNameApiView.as_view()),
]
