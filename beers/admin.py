from django.contrib import admin

# Register your models here.
from .models import Beer, Brewery, Style, Hop

admin.site.register(Beer)
admin.site.register(Brewery)
admin.site.register(Style)
admin.site.register(Hop)
