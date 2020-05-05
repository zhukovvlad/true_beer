from django.contrib import admin

# Register your models here.
from .models import Beer, Style, BeerComment

@admin.register(Beer)
class BeerAdmin(admin.ModelAdmin):
    list_display = ('title', 'version', 'brewery', 'date_pub', 'hunter', 'slug')

@admin.register(BeerComment)
class BeerCommentAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'beer', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('title', 'author', 'body')


admin.site.register(Style)
