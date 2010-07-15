from django.contrib import admin
from models import *


class OffsetAdmin(admin.ModelAdmin):
    pass

class ProjectAdmin(admin.ModelAdmin):
    pass

class ScanAdmin(admin.ModelAdmin):
    pass

class ScanCommentAdmin(admin.ModelAdmin):
    pass

#admin.site.register(Offset, OffsetAdmin)
#admin.site.register(Project, ProjectAdmin)
#admin.site.register(Scan, ScanAdmin)
#admin.site.register(ScanComment, ScanCommentAdmin)
