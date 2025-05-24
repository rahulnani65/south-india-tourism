from django.db import models
from django.contrib.auth.models import User

class State(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, help_text="A general overview of the state.")
    history = models.TextField(blank=True, help_text="Historical background of the state.")
    culture = models.TextField(blank=True, help_text="Cultural highlights, traditions, and festivals.")
    climate = models.TextField(blank=True, help_text="Climate information, including average temperatures and weather patterns.")
    best_time_to_visit = models.CharField(max_length=100, blank=True, help_text="Best months or seasons to visit the state.")
    favorites = models.ManyToManyField(User, related_name='favorite_states', blank=True)

    def __str__(self):
        return self.name

class Place(models.Model):
    CATEGORY_CHOICES = [
        ('Historical', 'Historical'),
        ('Natural', 'Natural'),
        ('Beach', 'Beach'),
        ('Cultural', 'Cultural'),
        ('Adventure', 'Adventure'),
    ]
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='places')
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    entry_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    visiting_hours = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Hotel(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='hotels')
    name = models.CharField(max_length=100)
    address = models.TextField()
    amenities = models.TextField(blank=True)
    distance = models.FloatField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='favorited_by')
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'place')

    def __str__(self):
        return f"{self.user.username} - {self.place.name}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.place.name} - {self.rating}"

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    favorites = models.ManyToManyField(User, related_name='favorite_posts', blank=True)

    def __str__(self):
        return self.title

class Itinerary(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='itineraries')
    day = models.IntegerField()
    activity = models.TextField()

    def __str__(self):
        return f"Day {self.day} Itinerary for {self.state.name}"

class TransportationOption(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='transport_options')
    mode = models.CharField(max_length=100)
    details = models.TextField()

    def __str__(self):
        return f"{self.mode} in {self.state.name}"
    
class Inquiry(models.Model):
    state = models.ForeignKey('State', on_delete=models.CASCADE, related_name='inquiries')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Inquiry from {self.name} for {self.state.name}"