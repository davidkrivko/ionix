import logging
import os
from datetime import datetime
import numpy as np

from streams.daos import RedisDao

# try:
#     import zoneinfo
# except ImportError:
#     from backports import zoneinfo
# from sqlalchemy import create_engine
#
# from sqlalchemy.pool import NullPool
# from sqlalchemy import desc
# from sqlalchemy import (
#     Table,
#     Column,
#     String,
#     DateTime,
#     MetaData,
#     SmallInteger,
#     Integer,
#     BigInteger,
#     Numeric,
#     Float,
#     Text,
# )
# from django.conf import settings
# from django.utils import timezone
# from sqlalchemy.sql.sqltypes import Boolean
# from streams.daos import RedisDao
#
dao = RedisDao()
# now = timezone.now
#
# IOT_DB_NAME = settings.IOT_DB_NAME
# IOT_DB_USER = settings.IOT_DB_USER
# IOT_DB_PASSWORD = settings.IOT_DB_PASSWORD
# IOT_DB_HOST = settings.IOT_DB_HOST
# THERMOSTAT_QUERY_LIMIT = 1
#
# DB_STRING = f"postgresql://{IOT_DB_USER}:{IOT_DB_PASSWORD}@{IOT_DB_HOST}/{IOT_DB_NAME}"
# db = create_engine(DB_STRING)
# meta = MetaData(db)
#
# # USER = os.environ.get("RDS_USERNAME")
# # HOST = os.environ.get("RDS_HOSTNAME")
# # DB_NAME = os.environ.get("RDS_DB_NAME")
# # PORT = os.environ.get("25060")
# # PASSWORD = os.environ.get("RDS_PASSWORD")
# #
# # DB = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}?sslmode=require"
# # db = create_engine(DB)
# # meta = MetaData(db)
#
#
# thermostatdata = Table(
#     "thermostatdata",
#     meta,
#     Column("sn", String),
#     Column("roomtemp", Numeric),
#     Column("settpoint", SmallInteger),
#     Column("status", SmallInteger),
#     Column("real_time", DateTime),
#     Column("id", BigInteger),
# )
#
#
# online_status = Table(
#     "online_status",
#     meta,
#     Column("sn", String),
#     Column("realtime", DateTime),
#     Column("id", BigInteger),
# )
#
# devicedata = Table(
#     "devicedata",
#     meta,
#     Column("sn", String),
#     Column("id", BigInteger),
#     Column("real_time", DateTime),
#     Column("time", DateTime),
#     Column("zone", String),
#     Column("endswitch", SmallInteger),
#     Column("icsmain", Float),
#     Column("icsz1", Float),
#     Column("icsz2", Float),
#     Column("icsz3", Float),
#     Column("icsboiler", Float),
#     Column("t1", SmallInteger),
#     Column("t2", SmallInteger),
#     Column("t3", SmallInteger),
#     Column("t4", SmallInteger),
#     Column("t5", SmallInteger),
#     Column("t6", SmallInteger),
#     Column("t7", SmallInteger),
#     Column("rt1", SmallInteger),
#     Column("rt2", SmallInteger),
#     Column("rt3", SmallInteger),
#     Column("ps", SmallInteger),
# )
#
# ioniqmaxdata = Table(
#     "ioniqmaxdata",
#     meta,
#     Column("sn", String),
#     Column("id", BigInteger),
#     Column("real_time", DateTime),
#     Column("endswitch", SmallInteger),
#     Column("icsmain", Float),
#     Column("icsz1", Float),
#     Column("icsz2", Float),
#     Column("icsz3", Float),
#     Column("icsboiler", Float),
#     Column("t1", SmallInteger),
#     Column("t2", SmallInteger),
#     Column("t3", SmallInteger),
#     Column("t4", SmallInteger),
#     Column("t5", SmallInteger),
#     Column("t6", SmallInteger),
#     Column("t7", SmallInteger),
#     Column("rt1", SmallInteger),
#     Column("rt2", SmallInteger),
#     Column("rt3", SmallInteger),
#     Column("ps", SmallInteger),
# )
#
# ioniqminidata = Table(
#     "ioniqminidata",
#     meta,
#     Column("id", BigInteger),
#     Column("sn", String),
#     Column("systemp", Numeric),
#     Column("endswitch", SmallInteger),
#     Column("real_time", DateTime),
# )
#
# devicevariables = Table(
#     "devicevariables",
#     meta,
#     Column("id", BigInteger),
#     Column("sn", String),
#     Column("rt1", SmallInteger),
#     Column("rt2", SmallInteger),
#     Column("rt3", SmallInteger),
#     Column("blr", SmallInteger),
#     Column("allof", SmallInteger),
#     Column("wifiid", Text),
#     Column("wifipass", Text),
#     Column("time", DateTime),
# )
#
# devicezonestatus = Table(
#     "devicezonestatus",
#     meta,
#     Column("id", BigInteger),
#     Column("sn", String),
#     Column("rt", SmallInteger),
#     Column("state", SmallInteger),
#     Column("time", DateTime),
# )
#
# wwsd = Table(
#     "wwsd",
#     meta,
#     Column("id", BigInteger),
#     Column("sn", String),
#     Column("setpoint", SmallInteger),
#     Column("enabled", Boolean),
#     Column("active", Boolean),
# )
#
# zip_temp_records = Table(
#     "zip_temp_records",
#     meta,
#     Column("id", BigInteger),
#     Column("zip_code", String),
#     Column("temp_f", SmallInteger),
#     Column("temp_c", SmallInteger),
#     Column("real_time", DateTime),
# )
#
# systemdata = Table(
#     "systemdata",
#     meta,
#     Column("id", BigInteger),
#     Column("sn", String),
#     Column("signal_level", SmallInteger),
#     Column("cpu_temp", SmallInteger),
#     Column("codebase_ver", String),
#     Column("last_reload_dt", DateTime),
#     Column("reloads_num", Integer),
#     Column("realtime", DateTime),
# )


def get_thermostat_data(serial_num: str) -> list:
    # data = []

    # try:
    #     with db.connect() as conn:
    #         select_statement = (
    #             thermostatdata.select()
    #             .where(thermostatdata.c.sn == serial_num)
    #             .order_by(desc("id"))
    #             .limit(THERMOSTAT_QUERY_LIMIT)
    #         )
    #         result_set = conn.execute(select_statement)
    #         for r in result_set:
    #             # print(f"DB parse response for {serial_num} {r} ")
    #             data.append(r)
    #     return data
    # except Exception as e:
    #     logging.error(f"Unable to fetch thermostat data from IoT db {e}")
    raise Exception("Deprecated")


def insert_controller_data(serial_num: str, systemp: int, endswitch: int):
    """Isert temperature update from ioniq controller
    to ioniqminidata table
    """
    # try:
    #     with db.connect() as conn:
    #         insert_statement = ioniqminidata.insert().values(
    #             sn=serial_num, systemp=systemp, endswitch=endswitch
    #         )
    #         conn.execute(insert_statement)
    #         return True
    # except Exception as e:
    #     logging.error(f"Error: unable to insert ioniqminidata to a table: {e}")
    raise Exception("Deprecated")


def insert_status_update(serial_num: str):
    """New record upon device API call"""
    # try:
    #     with db.connect() as conn:
    #         insert_statement = online_status.insert().values(sn=serial_num)
    #         conn.execute(insert_statement)
    # except Exception as e:
    #     logging.error(f"Unable to insert status update to IoT db: {e}")
    raise Exception("Deprecated")


def retrieve_status(serial_num: str):
    """Check online_status table and
    last record timestamp
    """
    # try:
    #     with db.connect() as conn:
    #         select_statement = (
    #             online_status.select()
    #             .where(online_status.c.sn == serial_num)
    #             .order_by(desc("id"))
    #             .limit(THERMOSTAT_QUERY_LIMIT)
    #         )
    #         result = conn.execute(select_statement).fetchone()
    #         return result
    # except Exception as e:
    #     logging.error(f"Unable to get last status update from IoT db: {e}")
    raise Exception("Deprecated")


def update_thermostat_data_on_change(
    serial_num: str, roomtemp: str, settpoint: str, status: str
) -> bool:
    """Make and INSERT into IoT db thermostatdata table

    Args:
        serial_num (str): [description]
        roomtemp (str): [description]
        settpoint (str): [description]
        status (str): [description]

    Returns:
        bool: returns True if executed successfully
    """
    # try:
    #     with db.connect() as conn:
    #         insert_statement = thermostatdata.insert().values(
    #             sn=serial_num,
    #             roomtemp=roomtemp,
    #             settpoint=settpoint,
    #             status=status,
    #         )
    #         conn.execute(insert_statement)
    #     return True
    # except Exception as e:
    #     logging.warning(str(e))
    #     return False
    raise Exception("Deprecated")


def fetch_ioniq_data(
    serial_num: str,
    extended: bool = False,
    endswitch_only: bool = False,
) -> dict:
    """Fetch controller data from devicedata table
    (ioniq max type with extended data available)

    Args:
        serial_num (str): device serial
        extended (bool): set False to fetch only ioniq minit endswitch data

    Returns:
        Dict: [description]
    """
    raise Exception("Deprecated")
    # table = None
    # # print("Fetching ioniq data", serial_num, extended)
    # if extended:
    #     table = ioniqmaxdata
    # else:
    #     table = ioniqminidata

    # if endswitch_only:
    #     select_statement = (
    #         table.select()
    #         .with_only_columns(table.c.endswitch)
    #         .where(table.c.sn == serial_num)
    #         .order_by(desc("id"))
    #         .limit(THERMOSTAT_QUERY_LIMIT)
    #     )
    # else:
    #     select_statement = (
    #         table.select()
    #         .where(table.c.sn == serial_num)
    #         .order_by(desc("id"))
    #         .limit(THERMOSTAT_QUERY_LIMIT)
    #     )

    # try:
    #     with db.connect() as conn:
    #         # print("Table", table)
    #         # print("DB conn", conn)
    #         # print("select_statement", select_statement)
    #         result = conn.execute(select_statement).fetchone()
    #         # print(result)
    #         if result is not None:
    #             return result._asdict()
    #         return result
    # except Exception as e:
    #     logging.error(f"Unable to fetch Ioniq data from IoT db: {e}")


#### UPD


def fetch_last_record(table: object, serial_num: str) -> dict:
    """
    Row utility function to execute SELECT statement.
    Not used directly.
    """
    raise Exception("Deprecated")
    # last_record = None
    # try:
    #     with db.connect() as conn:
    #         select_statement = (
    #             table.select().where(table.c.sn == serial_num).order_by(desc("id"))
    #         )
    #         result = conn.execute(select_statement).fetchone()
    #         if result is not None:
    #             last_record = result._asdict()
    # except Exception as e:
    #     logging.warning(f"Error: unable to fetch device variables to a table {e}")
    #     return (serial_num, e)
    # try:
    #     last_record.pop("time")
    # except:
    #     pass
    # return last_record


def fetch_device_variables_from_postgres(serial_num: str):
    """
    Searches for last device variables record in the postgres
    table. And creates default one if not found
    """
    raise Exception("Deprecated")
    # query_result = fetch_last_record(devicevariables, serial_num)

    # if query_result is not None:
    #     return query_result

    # # IF NEW DEVICE, CREATE DEFAULT ROW
    # init_record = dict(
    #     {
    #         "sn": serial_num,
    #         "rt1": 2,
    #         "rt2": 2,
    #         "rt3": 2,
    #         "blr": 2,
    #         "allof": 2,
    #         "wifiid": 0,
    #         "wifipass": 0,
    #         "time": now(),
    #     }
    # )
    # try:
    #     with db.connect() as conn:
    #         insert_statement = devicevariables.insert().values(**init_record)
    #         conn.execute(insert_statement)
    #     query_result = fetch_last_record(devicevariables, serial_num)
    # except Exception as e:
    #     logging.warning(f"Error: unable to insert to a device variables table {e}")
    #     query_result = None
    # return query_result


def fetch_device_variables(serial_num: str):
    """
    Fetch device variables for IoniqMax API
    """
    # Use redis im-memory hash object

    # data = dao.get_ionimax_variables_hash(serial_num)

    # if data is not None:
    #     return data

    # Legacy: use remote postgres db as a fallback
    # return fetch_device_variables_from_postgres(serial_num)
    raise Exception("Deprecated")


def update_device_variables_last_record(payload: dict) -> bool:
    """
    Update redis hash and postgres devicevariables table with new
    values
    """
    raise Exception("deprecated")
    # try:
    #     payload.pop("id")
    # except:
    #     return

    # dao.set_ioniqmax_variables_hash(payload)

    # # Update postgres
    # try:
    #     payload["time"] = now()
    #     with db.connect() as conn:
    #         insert_statement = devicevariables.insert().values(**payload)
    #         conn.execute(insert_statement)
    # except Exception as e:
    #     logging.warning(f"Error: unable to update to a device variables table {e}")
    #     return False


def change_device_variables(serial_num: str, pin_num: int, status: int) -> tuple:
    """
    Updates ioniqmax device variables rt1-rt3 in redis hash in-memory
    object. For ioniqmax (legacy) updates rt1-rt3 values
    in remote postgres db depending on simple switch signal
    Args:
        serial_num (str): ioniq_max serial number,
        status (int): 1 or 0 /zone one or off
        pin_num: zone number 1-3
    Returns:
        tuple: input args and "OK if success
    """

    # updated flow, inserts data to Redis hash first
    # key = f"rt{pin_num}"

    # has_payload = {
    #     "sn": serial_num,
    #     key: status,
    # }
    # dao.set_ioniqmax_variables_hash(payload=has_payload)

    # # update remote postgres table
    # last_record = fetch_device_variables(serial_num)
    # last_record[key] = status
    # response = update_device_variables_last_record(last_record)
    # return response
    raise Exception("Deprecated")


def force_upgrade_variables(serial_num: str, status: bool) -> tuple:
    """For ioniqmax (legacy) updates wifiid and wifipass
    based API request

    Args:
        serial_num (str): ioniq_max serial number
        status (bool): true for update

    Returns:
        tuple: input args and "OK if success
    """
    # last_record = fetch_device_variables(serial_num)

    # if status == True:
    #     last_record["wifiid"] = 1
    #     last_record["wifipass"] = 1
    # else:
    #     last_record["wifiid"] = 0
    #     last_record["wifipass"] = 0

    # try:
    #     last_record.pop("id")
    #     last_record["time"] = now()
    # except:
    #     pass
    # try:
    #     with db.connect() as conn:
    #         insert_statement = devicevariables.insert().values(**last_record)
    #         conn.execute(insert_statement)
    # except Exception as e:
    #     logging.warning(f"Error: unable to insert to a device variables table {e}")
    #     return (serial_num, status)

    # return (serial_num, status, "OK")
    raise Exception("Deprecated")


def fetch_devicezone_status(serial_num: str, pin_num: int):
    """Check devicezonestatus table if rt active or not"""

    # locate status based on thermostat / switch pin number
    # print("Fetching device zone status")
    # try:
    #     with db.connect() as conn:
    #         select_statement = (
    #             devicezonestatus.select()
    #             .where(
    #                 devicezonestatus.c.sn == serial_num,
    #                 devicezonestatus.c.rt == pin_num,
    #             )
    #             .order_by(desc("id"))
    #             .limit(THERMOSTAT_QUERY_LIMIT)
    #         )
    #         # print(select_statement)
    #         result = conn.execute(select_statement).fetchone()

    #         response = None

    #         if result is not None:
    #             response = result._asdict()
    #         # print(result)
    #         return response
    # except Exception as e:
    #     logging.error(f"Unable to fetch device zone status from IoT db: {e}")
    raise Exception("Deprecated")


def switch_boiler_supply(serial_num: str, value: int):
    """
    Update blr(endswitch) variable in ioniqmax variables hash,
    in-memory redis object.
    Legacy: locates controller variable in devicevariables table
    changes [blr] value according to the function input.
    Used with: Warm weather shutdown background task; Heating cycles opt. mode.
    """

    # hash_payload = {
    #     "sn": serial_num,
    #     "blr": value,
    # }
    # try:
    #     dao.set_ioniqmax_variables_hash(payload=hash_payload)
    # except Exception as e:
    #     logging.error("Unable to set ioniqmax vars to Redis hash")
    #     return str(e)
    #
    # # legacy: update remote postgres devicevariables table
    # last_record = fetch_device_variables(serial_num)
    # # print(f"Update device variables {serial_num}, value {value}")
    #
    # if last_record is not None:
    #     last_record["blr"] = value
    #     update_device_variables_last_record(last_record)
    raise Exception("Deprecated")


def insert_wwsd_data(serial_num: str, setpoint: int, enabled: bool, active: bool):
    """Insert wwsd data update from boiler settings changes"""

    raise Exception("Deprecated")
    # try:
    #     with db.connect() as conn:
    #         insert_statement = wwsd.insert().values(
    #             sn=serial_num, setpoint=setpoint, enabled=enabled, active=active
    #         )
    #         conn.execute(insert_statement)
    #         return True
    # except Exception as e:
    #     logging.warning(f"Error: unable to insert wwsd changes to a table: {e}")


# Extend IoniqMax API to write data


def insert_ioniqmax_device_data(data):
    """Insert ioniqmax device data"""
    # print(data)
    # data.pop("timestamp")
    # try:
    #     with db.connect() as conn:
    #         insert_statement = ioniqmaxdata.insert().values(**data)
    #         conn.execute(insert_statement)
    #         return True
    # except Exception as e:
    #     logging.warning(f"Error: unable to insert ioniqmax updates to a table: {e}")
    
    raise Exception("Deprecated")


def insert_ioniqmax_system_data(data):
    """Insert ioniqmax telemetry (signal, cpu temp etc.)"""
    # try:
    #     with db.connect() as conn:
    #         insert_statement = systemdata.insert().values(**data)
    #         conn.execute(insert_statement)
    #         return True
    # except Exception as e:
    #     logging.warning(f"Error: unable to insert ioniqmax updates to a table: {e}")
    raise Exception("Deprecated")


def insert_weather_data(zip_code: str, temp_f: int, temp_c: int, real_time=None):
    """
    Insert outdoor temperature records fetched for specific zip-code
    from weather.gov
    """
    # if real_time is None:
    #     real_time = now()
    # try:
    #     with db.connect() as conn:
    #         insert_statement = zip_temp_records.insert().values(
    #             zip_code=zip_code, temp_f=temp_f, temp_c=temp_c, real_time=real_time
    #         )
    #         conn.execute(insert_statement)
    #         return True
    # except Exception as e:
    #     logging.error(f"Error: unable to insert temperature records into a table: {e}")
    raise Exception("Deprecated")


def fetch_average_temp_by_date(date=None, zip_code=None) -> tuple:
    """
    Fetch temp records for specified zip code and date
    Returns calculated average
    """
    # temp_f_list = []
    # temp_c_list = []

    # # select_statement = zip_temp_records.select().where(zip_temp_records.c.zip_code == ZIP_CODE, zip_temp_records.c.real_time == str(DATE)).order_by(desc('id')).limit(10)
    # query = f"SELECT temp_f, temp_c FROM zip_temp_records WHERE zip_code='{zip_code}' AND DATE(real_time) = '{date}' ORDER BY id ASC"
    # print("query", query)
    # with db.connect() as conn:
    #     result_set = conn.execute(query).fetchall()
    #     print("result_set", result_set)
    #     for r in result_set:
    #         temp_f_list.append(r[0])
    #         temp_c_list.append(r[1])

    # np_list_f = np.array(temp_f_list)
    # print("np_list_f", np_list_f)
    # np_list_c = np.array(temp_c_list)
    # print("np_list_c", np_list_c)

    # w_aver_f = round(np.average(np_list_f))
    # w_aver_c = round(np.average(np_list_c))

    # return (w_aver_f, w_aver_c)
    raise Exception("Deprecated")


def fetch_controller_t2_temperature(controller_sn: str, date: None) -> list:
    """
    Fetch temp records for specified zip code and date
    Returns calculated average
    """
    # query = f"SELECT t2, real_time FROM ioniqmaxdata WHERE sn='{controller_sn}' AND DATE(real_time) = '{date}' ORDER BY id ASC"  # LIMIT {LIMIT}
    # # select_statement = ioniqmaxdata.select().with_only_columns(ioniqmaxdata.c.t2, ioniqmaxdata.c.real_time).where(ioniqmaxdata.c.sn == controller_sn, )
    # with db.connect() as conn:
    #     result_set = conn.execute(query).fetchall()
    #     return result_set
    raise Exception("Deprecated")
