from django.contrib import admin

# Register your models here.
from .models import Beer, Style, Hop

admin.site.register(Beer)
admin.site.register(Style)
admin.site.register(Hop)
