from django.db import models


# Create your models here.

class Region(models.Model):
    id = models.IntegerField('区域编号', primary_key=True)
    name = models.CharField('区域名字', max_length=30, null=False, blank=False)
    # 自关联
    parent = models.ForeignKey('self', verbose_name='父级区域', related_name='Children', on_delete=models.SET_NULL,
                               null=True, blank=True)
    # 经度
    longitude = models.FloatField('经度', null=True, blank=True)
    # 纬度
    latitude = models.FloatField('纬度', null=True, blank=True)
    # 三级区域划分 level 0 1 2 3
    level = models.CharField('区域级别', max_length=2, null=True, blank=True)

    # 标志 判断是否为直辖市 重庆 北京 上海 天津
    is_municipality = models.BooleanField('是否为直辖市', default=False, null=True)
    # 判断是否为省会城市
    is_provincial_city = models.BooleanField('是否为省会城市', default=False, null=True)
    # 判断是否为省直辖
    is_provincial_municipality = models.BooleanField('是否为省直辖', default=False, null=True)

    is_display = models.BooleanField('是否在地图上显示', default=False)

    def __str__(self):
        return self.name

    def get_province_name(self):
        if self.level == '0':
            return self.name
        elif self.level == '1':
            return self.parent.name
        elif self.level == '2':
            return self.parent.parent.name
        else:
            return self.name

    class Meta:
        verbose_name = '区域信息'
        verbose_name_plural = verbose_name
