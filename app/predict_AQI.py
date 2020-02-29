import logging
import sqlite3

import time

from app.predict_code_map import AQI_THRESHOLD, AQI_STR
from constants import CWB_DB_PATH, TABLE_AQFN, TABLE_AQI
from taiwan_area_map.query_area import query_area


def get_aqi_status_str(aqi):
    status = '良好'
    for i, t in enumerate(AQI_THRESHOLD):
        if aqi + 1 >= t:
            status = AQI_STR[i]
    return status


def predict_aqi(location):
    logger = logging.getLogger(__name__)
    now_ts = int(time.time())
    conn = sqlite3.connect(CWB_DB_PATH)
    area_list = query_area(location)

    if not area_list:
        return {}
    if len(area_list) >= 2:
        # multi-match, choose first as the area
        area_list = area_list[:1]

    area_list = area_list[0][0]
    c = conn.cursor()
    query_str = f'''
        SELECT publish_ts, forecast_ts, area, major_pollutant, AQI
        FROM {TABLE_AQFN}
        WHERE area=:area AND publish_ts = (
            SELECT MAX(publish_ts) FROM {TABLE_AQFN} WHERE area=:area
        ) AND forecast_ts > :min_ts
        ORDER BY forecast_ts ASC;
        '''
    c.execute(query_str, {'area': area_list, 'min_ts': now_ts - 12 * 3600})
    logger.debug(query_str)
    logger.debug('area: %s, min_ts: %s', area_list, now_ts - 12 * 3600)
    result = c.fetchone()
    publish_ts, forecast_ts, area_list, major_pollutant, aqi = result

    r_dict = {
        'publish_ts': publish_ts,
        'forecast_ts': forecast_ts,
        'area': area_list,
        'major_pollutant': major_pollutant if major_pollutant else '無',
        'AQI': aqi,
        'status': get_aqi_status_str(aqi),
    }

    conn.close()
    return r_dict


def query_aqi(county):
    logger = logging.getLogger(__name__)
    conn = sqlite3.connect(CWB_DB_PATH)
    c = conn.cursor()

    query_str = f'''
        SELECT MAX(publish_ts) FROM {TABLE_AQI} WHERE county=:county;
    '''
    logger.debug(query_str)
    logger.debug('county: %s', county)
    c.execute(query_str, {'county': county})
    (publish_ts,) = c.fetchone()
    publish_ts = int(publish_ts)

    query_str = f'''
        SELECT site_name, publish_ts, AQI, pollutant, status, PM10, PM25
        FROM {TABLE_AQI}
        WHERE county=:county AND publish_ts=:publish_ts;
        '''
    logger.debug(query_str)
    logger.debug('county: %s, publish_ts: %s', county, publish_ts)
    c.execute(query_str, {'county': county, 'publish_ts': publish_ts})
    result = c.fetchall()
    r_list = []
    for r in result:
        site_name, publish_ts, aqi, pollutant, status, pm10, pm25 = r
        r_list.append({
            'county': county,
            'site_name': site_name,
            'AQI': aqi,
            'pollutant': pollutant if pollutant else '無',
            'status': status,
            'PM10': pm10,
            'PM25': pm25,
        })

    conn.close()
    return r_list, publish_ts
