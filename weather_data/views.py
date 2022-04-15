from datetime import date
from django.shortcuts import render, redirect
from region.models import Region
from weather_data.models import WeatherData


# Create your views here.


def region_weather(request, region_id):
    region = Region.objects.get(id=region_id)
    data = WeatherData.objects.filter(region_id=region_id)[:7]
    provinces = Region.objects.filter(parent_id='0').exclude(id='0')
    cities = Region.objects.filter().exclude(parent_id='0')

    max_degrees = []
    min_degrees = []
    wind_class = []
    date_times = []
    for d in data:
        max_degrees.append(d.max_degree)
        min_degrees.append(d.min_degree)
        wind_class.append(d.day_wind_power)
        date_times.append(str(d.time))

    content = {
        'region': region,
        'data': data,
        'provinces': provinces,
        'cities': cities,
        'max_degrees': max_degrees,
        'min_degrees': min_degrees,
        'wind_class': wind_class,
        'date_times': date_times
    }
    return render(request, 'show.html', content)


# 最高温
def max_degree_show(request):
    region_list = Region.objects.filter(is_display=True)

    data = []
    geo_Coord = {}

    for r in region_list:
        data_dict = {'name': r.name, 'value': r.weatherdata_set.filter(time=date.today()).first().max_degree}
        data.append(data_dict)
        geo_Coord[r.name] = [r.longitude, r.latitude]

    content = {
        "data": data,
        "geo_Coord": geo_Coord
    }
    return render(request, 'max_degree_map.html', content)


# 最低温
def min_degree_show(request):
    region_list = Region.objects.filter(is_display=True)
    data = []
    geo_Coord = {}

    for r in region_list:
        data_dict = {'name': r.name, 'value': r.weatherdata_set.filter(time=date.today()).first().min_degree}
        data.append(data_dict)
        geo_Coord[r.name] = [r.longitude, r.latitude]

    content = {
        "data": data,
        "geo_Coord": geo_Coord
    }
    return render(request, 'min_degree_map.html', content)


def index(request):
    return render(request, 'index.html')


def get_search_region(request):
    region_name = request.GETa.get('city_name')
    region = Region.objects.get(name=region_name)
    data = WeatherData.objects.filter(region_id=region.id)[:7]
    provinces = Region.objects.filter(parent_id='0').exclude(id='0')
    cities = Region.objects.filter().exclude(parent_id='0')

    content = {
        'region': region,
        'data': data,
        'provinces': provinces,
        'cities': cities
    }
    return render(request, 'show.html', content)
