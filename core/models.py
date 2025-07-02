# =============================
# core/models.py
# Contains all database models for the core app
# =============================

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class State(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    history = models.TextField(blank=True)
    culture = models.TextField(blank=True)
    climate = models.TextField(blank=True)
    best_time_to_visit = models.TextField(blank=True)
    cultural_safety_tips = models.JSONField(default=list)
    favorites = models.ManyToManyField(User, related_name='favorite_states', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Place(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='places')
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    description = models.TextField()
    location = models.CharField(max_length=200, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    entry_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    visiting_hours = models.CharField(max_length=100, blank=True)
    safety_tip = models.TextField(blank=True)
    average_rating = models.FloatField(default=0.0)
    visit_count = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)

    favorited_by = models.ManyToManyField(User, related_name='favorite_places', blank=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Hotel(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='hotels')
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    amenities = models.CharField(max_length=200)
    distance = models.FloatField()  # Distance in kilometers from the place

    def __str__(self):
        return f"{self.name} near {self.place.name}"

class Cuisine(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cuisines')
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.state.name})"

class Restaurant(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='restaurants')
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    average_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.state.name})"

class Event(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='events')
    name = models.CharField(max_length=100)
    date = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.state.name})"

class Itinerary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='itineraries')
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='itineraries')
    day = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Day {self.day} Itinerary for {self.state.name} ({self.user.username})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, max_length=500)
    phone_number = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=100, blank=True)
    travel_style = models.CharField(max_length=50, blank=True)
    favorite_state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    total_places_visited = models.IntegerField(default=0)
    total_reviews = models.IntegerField(default=0)
    total_favorites = models.IntegerField(default=0)
    travel_bucket_list = models.JSONField(default=list)
    achievements = models.JSONField(default=list)
    ai_personality_analysis = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def update_stats(self):
        """Update user statistics"""
        self.total_places_visited = Favorite.objects.filter(user=self.user).count()
        self.total_reviews = self.user.review_set.count()
        self.total_favorites = Favorite.objects.filter(user=self.user).count() + self.user.favorite_states.count()
        self.save()
    
    def get_travel_level(self):
        """Get user's travel level based on activity"""
        total_activity = self.total_places_visited + self.total_reviews + self.total_favorites
        if total_activity >= 50:
            return "Travel Expert"
        elif total_activity >= 25:
            return "Travel Enthusiast"
        elif total_activity >= 10:
            return "Travel Explorer"
        else:
            return "Travel Beginner"

    def get_favorite_categories(self):
        """Return a list of unique categories from the user's favorited places. Returns an empty list if none."""
        try:
            favorite_places = self.user.favorite_places.all()
            categories = set()
            for place in favorite_places:
                if place.category:
                    categories.add(place.category)
            return list(categories)
        except Exception:
            return []

    def get_recent_activity(self):
        """Return a list of the user's 5 most recent favorites and 5 most recent reviews, sorted by date. Returns an empty list if none."""
        try:
            from core.models import Favorite, Review
            recent_favorites = Favorite.objects.filter(user=self.user).order_by('-created_at')[:5]
            recent_reviews = Review.objects.filter(user=self.user).order_by('-created_at')[:5]
            activity = []
            for fav in recent_favorites:
                activity.append({
                    'type': 'favorite',
                    'place': fav.place.name,
                    'date': fav.created_at
                })
            for rev in recent_reviews:
                activity.append({
                    'type': 'review',
                    'place': rev.place.name,
                    'rating': rev.rating,
                    'date': rev.created_at
                })
            # Sort all activity by date, descending
            activity.sort(key=lambda x: x['date'], reverse=True)
            return activity
        except Exception:
            return []

class Review(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='reviews')
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.place.name}"

class TelegramUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    telegram_username = models.CharField(max_length=100, unique=True)
    chat_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.telegram_username

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)  # Made optional
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'place')

    def __str__(self):
        return f"{self.user.username}'s favorite: {self.place.name}"

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='posts')
    favorites = models.ManyToManyField(User, related_name='favorite_posts', blank=True)  # Added for post favorites

    def __str__(self):
        return self.title

class TransportationOption(models.Model):
    TRANSPORT_TYPES = [
        ('BUS', 'Bus'),
        ('TRAIN', 'Train'),
        ('FLIGHT', 'Flight'),
        ('TAXI', 'Taxi'),
    ]
    
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='transportation_options')
    transport_type = models.CharField(max_length=10, choices=TRANSPORT_TYPES)
    name = models.CharField(max_length=100)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=50)  # e.g., "2 hours", "3 days"
    
    def __str__(self):
        return f"{self.get_transport_type_display()} - {self.name}"

class Inquiry(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='inquiries')
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    travel_dates = models.CharField(max_length=100, blank=True)
    travelers = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Inquiry from {self.name} - {self.email}"