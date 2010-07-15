from django.contrib import admin
from models import *


class WeatherStationAdmin(admin.ModelAdmin):
    pass

class WeatherTauAdmin(admin.ModelAdmin):
    pass

class TelescopeStatusAdmin(admin.ModelAdmin):
    pass

class PoolAdmin(admin.ModelAdmin):
    pass

class PoolPeriodAmin(admin.ModelAdmin):
    pass

#admin.site.register(WeatherStation, WeatherStationAdmin)
#admin.site.register(WeatherTau, WeatherTauAdmin)
#admin.site.register(PoolPeriod, PoolPeriodAmin)
