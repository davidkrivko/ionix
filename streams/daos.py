from abc import ABC, abstractmethod
from .schemas import StreamsKeySchema
from django_redis import get_redis_connection
from django.utils import timezone
from django.conf import settings
from .formatters import (
    convert_payload_datatypes,
    decode_redis_hash,
)
import devices
from typing import List

now = timezone.now

streams_key_schema = StreamsKeySchema()

REDIS_STREAM_MAX_LEN = settings.REDIS_STREAM_MAX_LEN


class AbstractDaoClass(ABC):
    @abstractmethod
    def add_thermostat_to_online_stream(self, sn, **kwargs):
        pass

    @abstractmethod
    def get_thermostat_from_online_stream(self, sn, **kwargs):
        pass

    @abstractmethod
    def add_ioniq_to_online_stream(self, sn, **kwargs):
        pass

    @abstractmethod
    def get_ioniq_from_online_stream(self, sn, **kwargs):
        pass

    @abstractmethod
    def add_thermostat_to_data_stream(self, payload, **kwargs):
        pass

    @abstractmethod
    def add_ioniq_to_data_stream(self, payload, **kwargs):
        pass

    @abstractmethod
    def get_thermostat_from_data_stream(self, sn, **kwargs):
        pass

    @abstractmethod
    def get_ioniq_from_data_stream(self, sn, **kwargs):
        pass

    @abstractmethod
    def set_ioniqmax_variables_hash(self, payload, **kwargs):
        pass

    @abstractmethod
    def get_ionimax_variables_hash(self, sn, **kwargs):
        pass

    @abstractmethod
    def save_boiler_controller_settings(self, payload, **kwargs):
        pass

    @abstractmethod
    def get_boiler_controller_settings(self, sn, **kwargs):
        pass


class RedisDao(AbstractDaoClass):
    """
    Instantiates Data Access object which uses
    redis to store iot data in its data types (streams, ts etc.)
    """

    MAXLEN = 86400  # max amount of records in a stream (oldest trimed)

    # ONLINE STATUS STREAMS

    def add_thermostat_to_online_stream(self, sn, **kwargs):

        key = streams_key_schema.thermostat_status_key(sn)
        connect = get_redis_connection("streams")
        timestamp = now()
        data = {"timestamp": f"{timestamp}"}

        s = connect.xadd(key, data, maxlen=self.MAXLEN)
        return s

    def get_thermostat_from_online_stream(self, sn, **kwargs):

        key = streams_key_schema.thermostat_status_key(sn)
        connect = get_redis_connection("streams")

        return connect.xrevrange(key, max="+", min="-", count=1)

    def add_ioniq_to_online_stream(self, sn, **kwargs):

        key = streams_key_schema.ioniq_status_key(sn)
        connect = get_redis_connection("streams")
        timestamp = now()
        data = {"timestamp": f"{timestamp}"}

        s = connect.xadd(key, data, maxlen=self.MAXLEN)
        return s

    def get_ioniq_from_online_stream(self, sn, **kwargs):

        key = streams_key_schema.ioniq_status_key(sn)
        connect = get_redis_connection("streams")
        return connect.xrevrange(key, max="+", min="-", count=1)

    # DATA STREAMS

    def add_thermostat_to_data_stream(self, payload, **kwargs):

        sn = payload["sn"]
        key = streams_key_schema.thermostat_data_key(sn)
        connect = get_redis_connection("streams")
        timestamp = now()
        payload["timestamp"] = f"{timestamp}"
        s = connect.xadd(key, payload, maxlen=self.MAXLEN)
        return s

    def add_ioniq_to_data_stream(self, payload, **kwargs):

        sn = payload["sn"]
        key = streams_key_schema.ioniq_data_key(sn)
        connect = get_redis_connection("streams")
        timestamp = now()
        payload["timestamp"] = f"{timestamp}"
        clean_data = convert_payload_datatypes(payload)
        s = connect.xadd(key, clean_data, maxlen=self.MAXLEN)
        return s

    def get_thermostat_from_data_stream(self, sn, **kwargs):
        key = streams_key_schema.thermostat_data_key(sn)
        connect = get_redis_connection("streams")
        return connect.xrevrange(key, max="+", min="-", count=1)

    def get_ioniq_from_data_stream(self, sn, **kwargs):

        key = streams_key_schema.ioniq_data_key(sn)
        connect = get_redis_connection("streams")
        return connect.xrevrange(key, max="+", min="-", count=1)

    def set_ioniqmax_variables_hash(self, payload, **kwargs):
        sn = payload["sn"]
        key = streams_key_schema.ioniq_vars_key(sn)
        connect = get_redis_connection("streams")
        # fast check for existing record
        is_empty = len(connect.hkeys(key)) == 0
        if is_empty:
            data = devices.utils.fetch_device_variables_from_postgres(sn)
            # populate with fetched payload
            init_dict = {
                "sn": sn,
                "rt1": data["rt1"],
                "rt2": data["rt2"],
                "rt3": data["rt3"],
                "blr": data["blr"],
                "wifiid": data["wifiid"],
                "wifipass": data["wifipass"],
            }
            connect.hmset(key, init_dict)
            pass
        return connect.hmset(key, payload)

    def get_ionimax_variables_hash(self, sn, **kwargs):
        key = streams_key_schema.ioniq_vars_key(sn)
        connect = get_redis_connection("streams")
        raw_data = connect.hgetall(key)
        data = decode_redis_hash(raw_data)
        return data

    def save_boiler_controller_settings(self, payload, **kwargs):
        sn = payload["sn"]
        key = streams_key_schema.boiler_settings_key(sn)
        connect = get_redis_connection("streams")
        return connect.hmset(key, payload)

    def get_boiler_controller_settings(self, sn, **kwargs):
        key = streams_key_schema.boiler_settings_key(sn)
        connect = get_redis_connection("streams")
        raw_data = connect.hgetall(key)
        data = decode_redis_hash(raw_data)
        return data

    def set_paired_relay_controller_data(self, sn: str, payload: dict):
        key = streams_key_schema.paired_relay_key(sn)
        timestamp = now()
        payload["timestamp"] = f"{timestamp}"
        connect = get_redis_connection("streams")
        return connect.hmset(key, payload)

    def get_paired_relay_controller_data(self, sn: str):
        key = streams_key_schema.paired_relay_key(sn)
        connect = get_redis_connection("streams")
        raw_data = connect.hgetall(key)
        data = decode_redis_hash(raw_data)
        return data

    def set_paired_thermostat_data(self, sn: str, payload: dict):
        key = streams_key_schema.paired_thermostat_key(sn)
        timestamp = now()
        payload["timestamp"] = f"{timestamp}"
        connect = get_redis_connection("streams")
        return connect.hmset(key, payload)

    def get_paired_thermostat_data(self, sn: str):
        key = streams_key_schema.paired_thermostat_key(sn)
        connect = get_redis_connection("streams")
        raw_data = connect.hgetall(key)
        data = decode_redis_hash(raw_data)
        return data

    def set_max_controller_related_thermostats(
        self, sn: str, thermostats_serials: List[str]
    ):
        key = streams_key_schema.ioniq_max_thermostats_hset_key(sn)
        connect = get_redis_connection("streams")
        return connect.sadd(key, *thermostats_serials)

    def get_max_controller_related_thermostats(self, sn: str):
        key = streams_key_schema.ioniq_max_thermostats_hset_key(sn)
        connect = get_redis_connection("streams")
        raw_data = connect.smembers(key)
        return [x.decode("utf-8") for x in raw_data]

    def set_thermostat_setpoint(self, sn: str, setpoint: str):
        TTL = 15
        key = streams_key_schema.thermostat_setpoint_key(sn)
        connect = get_redis_connection("streams")
        connect.set(key, setpoint)
        connect.expire(key, TTL)
        return

    def get_thermostat_setpoint(self, sn: str):
        key = streams_key_schema.thermostat_setpoint_key(sn)
        connect = get_redis_connection("streams")
        return connect.get(key)

    def set_boiler_data(self, sn: str, payload: dict):
        key = streams_key_schema.boiler_data_key(sn)
        connect = get_redis_connection("streams")
        return connect.hmset(key, payload)

    def get_boiler_data(self, sn: str):
        key = streams_key_schema.boiler_data_key(sn)
        connect = get_redis_connection("streams")
        raw_data = connect.hgetall(key)
        data = decode_redis_hash(raw_data)
        return data


redis_dao = RedisDao()
