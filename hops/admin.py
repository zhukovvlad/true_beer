from django.contrib import admin

# Register your models here.
from .models import Hop, AromaProfile

admin.site.register(Hop)
admin.site.register(AromaProfile)