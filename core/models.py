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

class Hotel(models.Model):
    AMENITIES = (
        ('wifi', 'Wi-Fi'),
        ('pool', 'Swimming Pool'),
        ('ac', 'Air Conditioning'),
        ('parking', 'Parking'),
        ('restaurant', 'Restaurant'),
        ('gym', 'Gym'),
    )

    name = models.CharField(max_length=100)
    tourist_place = models.ForeignKey(TouristPlace, on_delete=models.CASCADE, related_name='hotels')
    address = models.TextField(blank=True)
    amenities = models.CharField(max_length=200, blank=True)  # Comma-separated, e.g., "wifi,ac"
    distance_km = models.FloatField(null=True, blank=True)  # From tourist place
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} near {self.tourist_place.name}"

    class Meta:
        ordering = ['name']