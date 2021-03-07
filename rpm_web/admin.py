from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(MType_input)
admin.site.register(MProject)
admin.site.register(MVersion)
admin.site.register(MECU)
admin.site.register(MRelease_input)
