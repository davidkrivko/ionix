from datetime import datetime, time, date, timedelta
from .models import DeviceScheduleModel


def populate_schedule_options():
    """
    Check if schedule table is blank
    and populate it with objects (options)
    """

    queryset = DeviceScheduleModel.objects.all()

    if not queryset.exists():

        d = date(2021, 1, 1)
        delta = timedelta(minutes=15)

        for weekday in range(1, 8):

            t = time(0, 0)
            timestamp = datetime.combine(d, t)

            for i in range(0, 96):
                obj = DeviceScheduleModel(
                    week_day=weekday,
                    checkpoint=timestamp
                )
                obj.save()
                timestamp = timestamp + delta
