import os
from datetime import datetime, timedelta

import django
from django.db.models import Q

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_analysis.settings')
# 启动django
django.setup()

from weather_data.models import WeatherData
from region.models import Region
import requests

from weather_analysis.settings import PARAMS, URL, HEADERS


def get_region_weather(region: Region):
    params = PARAMS
    params['province'] = region.get_province_name()
    params['city'] = region.name
    res = requests.get(URL, params=PARAMS, headers=HEADERS)

    return res.json()['data']['forecast_24h']


def get_weather_by_display_region():
    region_list = Region.objects.filter(Q(level=1) | Q(is_municipality=1))
    # 对拿到的数据进行轮询
    for r in region_list:
        data = get_region_weather(r)
        if data:
            # 把天气信息保存到数据库中
            for v in data.values():
                WeatherData.objects.create(region=r, **v)
                print('%s天气已经成功保存' % r.name)


def delete_weather_by_region(region: Region):
    start = datetime.now() - timedelta(days=1)
    end = datetime.now() + timedelta(days=6)
    data = WeatherData.objects.filter(time__gte=start, time__lte=end, region=region)
    if data.count() > 0:
        print(data.delete())


def delete_all_weather():
    start = datetime.now() - timedelta(days=1)
    end = datetime.now() + timedelta(days=6)
    data = WeatherData.objects.filter(time__gte=start, time__lte=end)
    if data.count() > 0:
        print(data.delete())


if __name__ == '__main__':
    delete_all_weather()
    get_weather_by_display_region()

