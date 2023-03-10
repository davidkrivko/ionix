from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import HeatingDataDateRangeSerializer
from devices.models import IoniqControllerModel
from .utils import count_heating_cycles
from dateutil.relativedelta import relativedelta
from devices.utils import (
    fetch_average_temp_by_date,
)


class FetchHeatingCyclesAndWeatherDataApiView(APIView):
    """
    Allow front-end to request calculation on heating
    cycles along with outdoor temp values for specified
    date range (for Ioniqmax only @NB)
    """

    def post(self, request):
        ctx = {
            'detail': None,
            'data': None,
        }
        serializer = HeatingDataDateRangeSerializer(data = request.data)

        if serializer.is_valid(raise_exception=True):
            owner = request.user.owner
            sn = serializer.validated_data.get("sn")
            start_date = serializer.validated_data.get("start_date")
            end_date = serializer.validated_data.get("end_date")

            controller = IoniqControllerModel.objects.select_related('building').get(serial_num=sn, model_type="MX") # owner = owner
            zip = controller.building.zip_code.zip_code
            print("controller", controller)

            # try:
            #     controller = IoniqControllerModel.objects.select_related('building').get(sn=sn) # owner = owner
            #     zip = controller.building.zip_code
            #     print("controller", controller)
            # except:
            #     ctx['detail'] = "Unable to locate specified controller"
            #     return Response(ctx, status = 404)

            delta = end_date - start_date
            date_cycles_count = []
            date_labels = []
            date_temp_list_f = []
            date_temp_list_c = []

            for i in range(delta.days + 1):
                print("i", i)
                date = start_date + relativedelta(days=i)
                print("date", date)
                cycles = count_heating_cycles(controller_sn = sn, date=date)
                temp_data = fetch_average_temp_by_date(date, zip_code=zip)
                date_cycles_count.append(cycles)
                day_label = date.strftime("%d %b")
                date_labels.append(day_label)
                
                if temp_data is not None:
                    date_temp_list_f.append(temp_data[0])
                    date_temp_list_c.append(temp_data[1])
                else:
                    pass

            ctx['data'] = {
                "date_cycles_count": date_cycles_count,
                "date_labels": date_labels,
                "date_temp_list_f": date_temp_list_f,
                "date_temp_list_c": date_temp_list_c,
            }

            return Response(ctx, status=200)