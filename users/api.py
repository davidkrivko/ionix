from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from django.contrib import messages
from django_q.tasks import async_task

from properties.models import ApartmentModel
from .serializers import (
    NameSerializer,
    PasswordUpdateSerializer,
    UserIdSerializer,
)


class ProfileDataApiView(APIView):
    """Return current user role and profile data"""

    def get(self, request):
        ctx = {
            "detail": None,
            "data": None,
        }
        try:
            owner = request.user.owner
        except:
            owner = None

        if owner is not None:
            logo = None
            if owner.logo:
                logo = owner.logo.url
            boiler = owner.boilers.first()

            ctx["data"] = {
                "profile": "owner",
                "email": request.user.username,
                "is_landlord": owner.is_landlord,
                "first_name": owner.first_name,
                "nickname": owner.nickname,
                "phone_number": str(owner.phone_number),
                "logo": logo,
                # "boiler_id": boiler.pk,
            }
        try:
            tenant = request.user.tenant
        except:
            tenant = None

        if tenant is not None:
            logo = None
            if tenant.logo:
                logo = tenant.logo.url

            ctx["data"] = {
                "email": request.user.username,
                "profile": "tenant",
                "first_name": tenant.first_name,
                "is_guest": tenant.is_guest,
                "logo": logo,
                "password_reset_needed": tenant.password_reset_needed,
            }

        return Response(ctx, status=200)


class UpdateTenantNameApiView(APIView):
    """Allow tenants to update their name"""

    permission_classes = [IsAuthenticated]

    def post(self, request):

        ctx = {
            "detail": None,
            "data": None,
        }

        serializer = NameSerializer(data=request.data)

        if serializer.is_valid():

            first_name = serializer.validated_data.get("first_name")
            email = serializer.validated_data.get("email")

            try:
                tenant = request.user.tenant
            except:
                ctx["detail"] = "Current user doesn't have tenant profile"
                return Response(ctx, status=403)

            if len(first_name) < 3:
                ctx["detail"] = "Name or nickname is too short"
                return Response(ctx, status=400)

            tenant.first_name = first_name
            tenant.save()

            if email is not None and len(email) > 5:
                user = request.user
                user.username = email
                user.save()

            ctx["detail"] = "Profile was successfully updated"
            messages.success(
                request, "You've updated your profile data. Please, log in now."
            )
            return Response(ctx, status=200)

        return Response(ctx, status=500)


class UpdateOwnerProfileApiView(APIView):
    """Allow tenants to update their name"""

    permission_classes = [IsAuthenticated]

    def post(self, request):

        ctx = {
            "detail": None,
            "data": None,
        }

        serializer = NameSerializer(data=request.data)

        if serializer.is_valid():

            first_name = serializer.validated_data.get("first_name")
            email = serializer.validated_data.get("email")

            try:
                owner = request.user.owner
            except:
                ctx["detail"] = "Current user doesn't have owners profile"
                return Response(ctx, status=403)

            if len(first_name) < 3:
                ctx["detail"] = "Name or nickname is too short"
                return Response(ctx, status=400)

            owner.first_name = first_name
            owner.save()

            if email is not None and len(email) > 5:
                user = request.user
                user.username = email
                user.save()

            logout(request)

            ctx["detail"] = "Profile was successfully updated"
            messages.success(
                request, "You've updated your profile data. Please, log in now."
            )
            return Response(ctx, status=200)

        return Response(ctx, status=500)


class UpdateTenantPasswordApiView(APIView):
    """
    Allow tenants to update their password
    withing profile page (whilte authenticated)
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        ctx = {
            "detail": None,
            "data": None,
        }
        serializer = PasswordUpdateSerializer(data=request.data)

        if serializer.is_valid():

            old_password = serializer.validated_data.get("old_password")
            new_password = serializer.validated_data.get("new_password")

            user = request.user
            first_login = False

            try:
                tenant = user.tenant
                if tenant.password_reset_needed == True:
                    first_login = True
            except:
                pass

            if not first_login:
                if not user.check_password(old_password):
                    ctx["detail"] = "Wrong password"
                    return Response(ctx, status=403)

            user.set_password(new_password)
            user.save()

            # if tenant first login update its profile
            try:
                tenant = user.tenant
                async_task(
                    "users.utils.update_tenant_password_reset_success", tenant.pk
                )
            except:
                pass

            ctx["detail"] = "Password was successfully updated"
            logout(request)
            messages.success(
                request, "You've updated your profile data. Please, log in now."
            )
            return Response(ctx, status=200)
