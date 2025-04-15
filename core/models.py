from django.db import models

class State(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class TouristPlace(models.Model):
    CATEGORIES = (
        ('historical', 'Historical'),
        ('natural', 'Natural'),
        ('cultural', 'Cultural'),
        ('beach', 'Beach'),
        ('hill_station', 'Hill Station'),
    )

    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='places')
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORIES)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}, {self.state.name}"

    class Meta:
        ordering = ['name']

class Restaurant(models.Model):
    DIETARY_TAGS = (
        ('vegetarian', 'Vegetarian'),
        ('vegan', 'Vegan'),
        ('gluten_free', 'Gluten-Free'),
        ('south_indian', 'South Indian'),
        ('north_indian', 'North Indian'),
        ('chinese', 'Chinese'),
    )

    name = models.CharField(max_length=100)
    tourist_place = models.ForeignKey(TouristPlace, on_delete=models.CASCADE, related_name='restaurants')
    address = models.TextField(blank=True)
    dietary_tags = models.CharField(max_length=200, blank=True)  # Comma-separated, e.g., "vegetarian,vegan"
    distance_km = models.FloatField(null=True, blank=True)  # From tourist place
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} near {self.tourist_place.name}"

    class Meta:
        ordering = ['name']