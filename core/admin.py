from django.contrib import admin
from .models import State, TouristPlace, Restaurant

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(TouristPlace)
class TouristPlaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'state', 'category']
    list_filter = ['state', 'category']
    search_fields = ['name']

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'tourist_place', 'dietary_tags']
    list_filter = ['tourist_place']
    search_fields = ['name', 'dietary_tags']