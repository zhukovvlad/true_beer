from django.contrib import admin

# Register your models here.
from .models import Beer, Style

admin.site.register(Beer)
admin.site.register(Style)
