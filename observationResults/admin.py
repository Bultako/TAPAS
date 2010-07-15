from django.contrib import admin
from models import *


class FocusResultsAdmin(admin.ModelAdmin):
    pass

class PointingResultsAdmin(admin.ModelAdmin):
    pass

class CalibrationResultsAdmin(admin.ModelAdmin):
    pass

#admin.site.register(FocusResults, FocusResultsAdmin)
#admin.site.register(PointingResults, PointingResultsAdmin)
#admin.site.register(CalibrationResults, CalibrationResultsAdmin)
