import numpy as np
from scipy.signal import argrelextrema
import pandas as pd
from devices.utils import (
    fetch_controller_t2_temperature,
    fetch_average_temp_by_date,
)


def count_heating_cycles(controller_sn: str, date = None) -> int:
    """Calculates number of heating cycles
    for specified date based on endswitch value

    Args:
        date ([datetime.date]): date to fetch data
    """

    result = fetch_controller_t2_temperature(controller_sn, date)

    data = tuple(tuple([x[0]]) for x in result)
    x_time_series = tuple(x[1] for x in result)


    df = pd.DataFrame(data, index=x_time_series, columns=["t2"])   
    df_resampled = df.resample("5min").mean()

    t2_ilocs_min = argrelextrema(df_resampled.t2.values, np.less_equal, order=3)[0]
    t2_ilocs_max = argrelextrema(df_resampled.t2.values, np.greater_equal, order=3)[0]

    first_max_time_point = df_resampled.iloc[t2_ilocs_max].index[0]
    first_min_time_point = df_resampled.iloc[t2_ilocs_min].index[0]
    last_max_time_point = df_resampled.iloc[t2_ilocs_max].index[-1]
    last_min_time_point = df_resampled.iloc[t2_ilocs_min].index[-1]
    
    if first_min_time_point > first_max_time_point:
        t2_ilocs_max = t2_ilocs_max[1:]
    if last_min_time_point > last_max_time_point:
        t2_ilocs_min = t2_ilocs_min[:-1]

    # ax = df_resampled.plot(kind="line", grid=True, x_compat=True) 

    cycles_count = len(t2_ilocs_max)

    # print("cycles_count", cycles_count)
    return cycles_count


# print("date_labels", date_labels)
# print("date_cycles_count", date_cycles_count)
# print("date_temp_list_f", date_temp_list_f)
# print("date_temp_list_c", date_temp_list_c)