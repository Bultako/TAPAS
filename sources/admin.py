from django.contrib import admin
from models import *


class PredefinedSourceAdmin(admin.ModelAdmin):
    pass

class ObservedSourceAdmin(admin.ModelAdmin):
    pass


#admin.site.register(PredefinedSource, PredefinedSourceAdmin)
#admin.site.register(ObservedSource, ObservedSourceAdmin)
