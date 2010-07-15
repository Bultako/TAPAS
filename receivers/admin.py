from django.contrib import admin
from models import *


class PredefinedReceiverAdmin(admin.ModelAdmin):
    pass

class ReceiverAdmin(admin.ModelAdmin):
    pass

class RxReceiverCfgAdmin(admin.ModelAdmin):
    pass

class RxBolometerCfgAmin(admin.ModelAdmin):
    pass

#admin.site.register(PredefinedReceiver, PredefinedReceiverAdmin)
#admin.site.register(Receiver, ReceiverAdmin)
#admin.site.register(RxReceiverCfg, RxReceiverCfgAdmin)
#admin.site.register(RxBolometerCfg, RxBolometerCfgAmin)
