from django.contrib import admin

# Register your models here.
from .models import Brewery

@admin.register(Brewery)
class BreweryAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    list_filter = ('country',)

'''@admin.register(BeerComment)
class BeerCommentAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'beer', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('title', 'author', 'body')'''
