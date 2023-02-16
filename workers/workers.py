from properties.models import ZipCodeModel
from schedules.models import DeviceScheduleModel
from django_q.tasks import async_iter, async_task, schedule
from django.utils import timezone
from datetime import timedelta


def update_weather_on_zips():
    """Iterates over all ZipCode records
    and schedules background tasks to update
    temperature field (last observed)
    """
    now = timezone.now()
    iter = [obj.pk for obj in ZipCodeModel.objects.all()]

    async_iter("api.utils.parse_temp_from_weathergov", iter)
    wwsd_next_check_in = now + timedelta(minutes=5)
    schedule(
        "workers.tasks.trigger_warm_weather_shutdown_check",
        schedule_type="O",
        next_run=wwsd_next_check_in,  # wait few minutes
        # repeats=0, # do not repeat / run once
    )


def check_scheduled_objects():
    """Looks through DeviceScheduleModel for
    objects with current %H:%M timestamp and weekday part
    and passes it to task for futher proceeding
    """
    # print("Looking for scheduling list with current timestamp")
    now = timezone.localtime(timezone.now())
    # print("Now hour", now.hour)
    # print("Now minute", now.minute)
    # print("Current H:M", now.strftime("%H:%M"))
    # print("Weekday", now.isoweekday())
    queryset = DeviceScheduleModel.objects.filter(
        checkpoint__hour=now.hour,
        checkpoint__minute__range=(now.minute - 2, now.minute),
        week_day=now.isoweekday(),
    )
    # print("Queryset", queryset)

    if not queryset.exists():
        # print("Doing nothing")
        return
    schedule_list = queryset.first()
    # print("Found a list for", now.strftime("%H:%M"))
    async_task("workers.tasks.reset_thermostat_with_schedule", schedule_list.pk)
    # async_task("workers.tasks.reset_switches_with_schedule", schedule_list.pk)
    # async_task(
    #     "workers.tasks.reset_analogue_thermostats_with_schedule", schedule_list.pk
    # )
