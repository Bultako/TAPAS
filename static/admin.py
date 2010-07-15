from django.contrib import admin
from models import *


class stPredefinedCommentsAdmin(admin.ModelAdmin):
    pass

class stPointingModelsAdmin(admin.ModelAdmin):
    pass

class stRxNamesAdmin(admin.ModelAdmin):
    pass

class stProjectModesAdmin(admin.ModelAdmin):
    pass

class stBkNamesAdmin(admin.ModelAdmin):
    pass

class stObservingModesAdmin(admin.ModelAdmin):
    pass

class stFileLocationsAdmin(admin.ModelAdmin):
    pass

class stSoftwareVersionsAdmin(admin.ModelAdmin):
    pass

class stTelescopeStatesAdmin(admin.ModelAdmin):
    pass

class stSwitchingModesAdmin(admin.ModelAdmin):
    pass

class stSystemNamesAdmin(admin.ModelAdmin):
    pass


admin.site.register(stPredefinedComments, stPredefinedCommentsAdmin)
admin.site.register(stPointingModels, stPointingModelsAdmin)
admin.site.register(stRxNames, stRxNamesAdmin)
admin.site.register(stProjectModes, stProjectModesAdmin)
admin.site.register(stBkNames, stBkNamesAdmin)
admin.site.register(stObservingModes, stObservingModesAdmin)
admin.site.register(stFileLocations, stFileLocationsAdmin)
admin.site.register(stSoftwareVersions, stSoftwareVersionsAdmin)
admin.site.register(stTelescopeStates, stTelescopeStatesAdmin)
admin.site.register(stSwitchingModes, stSwitchingModesAdmin)
admin.site.register(stSystemNames, stSystemNamesAdmin)
