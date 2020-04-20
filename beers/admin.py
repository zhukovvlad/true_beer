from django.contrib import admin

# Register your models here.
from .models import Beer, Style

@admin.register(Beer)
class BeerAdmin(admin.ModelAdmin):
    list_display = ('title', 'version', 'brewery', 'date_pub', 'hunter', 'slug')


admin.site.register(Style)
