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
# from django.contrib import admin
# from .models import State, Place, Hotel, Contact


# admin.site.register(State)
# admin.site.register(Place)
# admin.site.register(Hotel)
# admin.site.register(Contact)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import State, Place, Hotel, Cuisine, Restaurant, Event, Itinerary, UserProfile, Review, TelegramUser, Favorite

# Unregister the default UserAdmin
admin.site.unregister(User)

# Register a custom UserAdmin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Fields to display in the list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_active', 'is_staff')
    # Fields to filter by in the list view
    list_filter = ('is_staff', 'is_active', 'date_joined')
    # Fields to search
    search_fields = ('username', 'email', 'first_name', 'last_name')
    # Fields to display in the detail view
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    # Fields to display when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    ordering = ('-date_joined',)  # Sort by date joined (newest first)

# Custom admin for State model with Favorites feature
@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_favorite', 'description')  # Display fields in the list view
    list_filter = ('favorites',)  # Add a filter for favorites
    actions = ('mark_as_favorite', 'remove_from_favorites')  # Custom admin actions
    search_fields = ('name',)  # Allow searching by name

    def get_queryset(self, request):
        # Store the request object to access the current user
        self.request = request
        return super().get_queryset(request)

    def is_favorite(self, obj):
        # Check if the current state is a favorite for the logged-in user
        return obj.favorites.filter(id=self.request.user.id).exists()
    is_favorite.boolean = True  # Display as a checkbox icon
    is_favorite.short_description = 'Favorite'  # Column header

    def mark_as_favorite(self, request, queryset):
        # Add selected states to the current user's favorites
        for state in queryset:
            state.favorites.add(request.user)
        self.message_user(request, "Selected states have been added to your favorites.")
    mark_as_favorite.short_description = "Mark selected states as favorite"

    def remove_from_favorites(self, request, queryset):
        # Remove selected states from the current user's favorites
        for state in queryset:
            state.favorites.remove(request.user)
        self.message_user(request, "Selected states have been removed from your favorites.")
    remove_from_favorites.short_description = "Remove selected states from favorites"

    # Add a custom view for favorited states
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('my-favorites/', self.admin_site.admin_view(self.my_favorites_view), name='my-favorites'),
        ]
        return custom_urls + urls

    def my_favorites_view(self, request):
        # Get the current user's favorited states
        favorites = State.objects.filter(favorites=request.user)
        context = {
            'favorites': favorites,
            'title': 'My Favorite States',
        }
        return render(request, 'admin/my_favorites.html', context)

    # Add custom CSS for styling
    class Media:
        css = {
            'all': ('css/admin-custom.css',)
        }

# Register other models
# admin.site.register(Place)  # Removed to avoid AlreadyRegistered error
admin.site.register(Hotel)
admin.site.register(Cuisine)
admin.site.register(Restaurant)
admin.site.register(Event)
admin.site.register(Itinerary)
admin.site.register(UserProfile)
admin.site.register(Review)
admin.site.register(TelegramUser)

# Register the Favorite model for admin management
admin.site.register(Favorite)

# Enhanced Place admin to show favorites info
@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'category', 'favorite_count')
    list_filter = ('state', 'category', 'favorited_by')
    search_fields = ('name',)

    def favorite_count(self, obj):
        return obj.favorited_by.count()
    favorite_count.short_description = 'Number of Favorites'