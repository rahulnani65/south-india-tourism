# from django.contrib import admin
# from .models import State, TouristPlace, Hotel

# @admin.register(State)
# class StateAdmin(admin.ModelAdmin):
#     list_display = ['name', 'created_at']           # source env/bin/activate
#     search_fields = ['name']

# @admin.register(TouristPlace)
# class TouristPlaceAdmin(admin.ModelAdmin):
#     list_display = ['name', 'state', 'category']
#     list_filter = ['state', 'category']
#     search_fields = ['name']

# @admin.register(Hotel)
# class HotelAdmin(admin.ModelAdmin):
#     list_display = ['name', 'tourist_place', 'amenities']
#     list_filter = ['tourist_place']
#     search_fields = ['name', 'amenities']
from django.contrib import admin
from .models import State, Place, Hotel, Contact

admin.site.register(State)
admin.site.register(Place)
admin.site.register(Hotel)
admin.site.register(Contact)