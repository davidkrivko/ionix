from streams.daos import RedisDao
from django.utils import dateparse, timezone
from django.conf import settings
from django_redis import get_redis_connection

now = timezone.now

DEVICE_ONLINE_STATUS_DELTA_SEC = settings.DEVICE_ONLINE_STATUS_DELTA_SEC
dao = RedisDao()


def flush_redis_streams(self):
    get_redis_connection("streams").flushall()


def fetch_online_status_from_online_stream(sn: str, device: str) -> object:
    """
    Searches serial number in redis stream of devices online status
    and returns bool response in a context object

    Args:
        sn (str): device serial number
        device (str): device type (TRM - thermostat, ION - controller)

    Returns:
        object: [data] (bool) True if online, else False
    """

    ctx = {
        'detail': None,
        'data': None, 
    }
    if device == "TRM":
        record = dao.get_thermostat_from_online_stream(sn)
    else:
        record = dao.get_ioniq_from_online_stream(sn)
    
    if len(record) == 0:
        ctx['detail'] = 'No records found for the serial specified'
        ctx['data'] = False
        return ctx

    timestamp_str = record[0][1][b'timestamp'].decode('utf-8')
    timestamp = dateparse.parse_datetime(timestamp_str)
    delta = now() - timestamp
    
    if delta.seconds <= DEVICE_ONLINE_STATUS_DELTA_SEC:
        ctx['data'] = True
        ctx['detail'] = f"Timedelta (last seen online) [{delta.seconds} s]"
    else:
        ctx['data'] = False
        ctx['detail'] = f"Timedelta (last seen online) [{delta.seconds} s] " \
                        f"status exceeds limit [{DEVICE_ONLINE_STATUS_DELTA_SEC} s]"

    return ctx


def fetch_device_data_from_data_stream(sn: str, device: str) -> object:
    """Searches serial number in redis stream of devices data
    and returns payload in response object

    Args:
        sn (str): device serial number
        device (str): device type (TRM - thermostat, ION - controller)

    Returns:
        object: ctx[data] device related data
    """

    ctx = {
        'detail': None,
        'data': None, 
    }
    if device == "TRM":
        record = dao.get_thermostat_from_data_stream(sn)
    else:
        record = dao.get_ioniq_from_data_stream(sn)
   
    if len(record) == 0:
        ctx['detail'] = 'No records found for the serial specified'
        ctx['data'] = False
        return ctx

    payload = dict()
    binary_dict = record[0][1]
    
    for key, value in binary_dict.items():
        payload[key.decode('utf-8')] = value.decode('utf-8')

    ctx['data'] = payload
    return ctx
