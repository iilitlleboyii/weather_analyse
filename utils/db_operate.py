import csv
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_analysis.settings')
django.setup()

from region.models import Region


def level_update():
    print(Region.objects.filter(parent_id=0).exclude(id=0).update(level='0'))
    print(Region.objects.filter(parent__level='0').update(level='1'))
    print(Region.objects.filter(parent__level='1').update(level='2'))
    print(Region.objects.filter(parent__level='2').update(level='3'))


# 生成直辖市
def generate_municipality():
    print(Region.objects.filter(name__in=['北京市', '上海市', '天津市', '重庆市']).update(is_municipality=True))


# 生成省会城市
def generate_provincial_city():
    print(Region.objects.filter(id__endswith='0100').exclude(parent__is_municipality=True).update(
        is_provincial_city=True))


# 生成省直辖市
def generate_provincial_municipality():
    print(Region.objects.filter(parent__name__in=['省直辖行政单位', '省直辖县级行政单位']).update(is_provincial_municipality=True))


def insert_latitude_longitude_from_csv():
    with open('中国省市经纬度.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)

        for row in reader:
            if row[0] == 'province':
                continue
            if row[1] == '':
                r = Region.objects.filter(name=row[0]).first()
            elif row[1] != '':
                r = Region.objects.filter(name=row[1]).first()
            if r:
                r.longitude = float(row[2])
                r.latitude = float(row[3])
                r.save()
                print('%s修改成功' % r.name)


if __name__ == '__main__':
    level_update()
    generate_municipality()
    generate_provincial_city()
    generate_provincial_municipality()
    insert_latitude_longitude_from_csv()
