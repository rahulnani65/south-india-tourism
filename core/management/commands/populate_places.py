from django.core.management.base import BaseCommand
from core.models import State, Place, Cuisine, Restaurant, Event, Itinerary

class Command(BaseCommand):
    help = 'Populates the database with initial data for South India Tourism'

    def handle(self, *args, **kwargs):
        # Delete existing Tamil Nadu data to avoid duplicates
        State.objects.filter(name="Tamil Nadu").delete()

        # Create Tamil Nadu state
        tamil_nadu, created = State.objects.get_or_create(
            name="Tamil Nadu",
            slug="tamil-nadu",
            defaults={
                'description': 'Tamil Nadu, a South Indian state, is famed for its Dravidian-style Hindu temples, rich cultural heritage, and vibrant festivals.',
                'history': 'Tamil Nadu has a history dating back to the Sangam period (300 BCE - 300 CE), with a legacy of Chola, Chera, and Pandya dynasties.',
                'culture': 'Known for classical Tamil literature, Carnatic music, Bharatanatyam dance, and traditional silk sarees.',
                'climate': 'Tropical climate with monsoon seasons; summers are hot, winters are mild.',
                'best_time_to_visit': 'October to March is the best time to visit Tamil Nadu.',
                'cultural_safety_tips': [
                    "Respect temple dress codes by wearing modest clothing.",
                    "Remove shoes before entering religious sites.",
                    "Avoid public displays of affection in conservative areas."
                ]
            }
        )

        # Places in Tamil Nadu with coordinates
        places = [
            {
                'name': 'Meenakshi Temple',
                'category': 'religious',
                'description': 'A historic Hindu temple with towering gopurams, dedicated to Goddess Meenakshi.',
                'location': 'Madurai',
                'latitude': 9.9195,
                'longitude': 78.1192,
                'entry_fee': 50,
                'visiting_hours': '9 AM - 7 PM',
                'safety_tip': 'Beware of crowded areas inside the temple.',
            },
            {
                'name': 'Marina Beach',
                'category': 'natural',
                'description': 'One of the longest urban beaches in the world, perfect for a sunrise stroll.',
                'location': 'Chennai',
                'latitude': 13.0500,
                'longitude': 80.2824,
                'entry_fee': 0,
                'visiting_hours': 'Open 24 hours',
                'safety_tip': 'Avoid swimming due to strong currents.',
            },
            {
                'name': 'Mahabalipuram',
                'category': 'historical',
                'description': 'A UNESCO World Heritage site with ancient rock-cut temples and sculptures.',
                'location': 'Near Chennai',
                'latitude': 12.6208,
                'longitude': 80.1945,
                'entry_fee': 500,
                'visiting_hours': '6 AM - 6 PM',
                'safety_tip': 'Wear sunscreen as it can get very sunny.',
            },
            {
                'name': 'Ooty Hill Station',
                'category': 'natural',
                'description': 'A scenic hill station in the Nilgiris, known for its tea plantations and cool climate.',
                'location': 'Ooty',
                'latitude': 11.4102,
                'longitude': 76.6950,
                'entry_fee': 0,
                'visiting_hours': 'Open 24 hours',
                'safety_tip': 'Carry warm clothing for the chilly evenings.',
            },
        ]

        for place_data in places:
            Place.objects.get_or_create(
                state=tamil_nadu,
                name=place_data['name'],
                defaults={
                    'category': place_data['category'],
                    'description': place_data['description'],
                    'location': place_data['location'],
                    'latitude': place_data['latitude'],
                    'longitude': place_data['longitude'],
                    'entry_fee': place_data['entry_fee'],
                    'visiting_hours': place_data['visiting_hours'],
                    'safety_tip': place_data['safety_tip'],
                    'average_rating': 4.5,
                    'visit_count': 100,
                }
            )

        # Add cuisines
        cuisines = [
            {'name': 'Dosa', 'description': 'A crispy pancake made from rice and urad dal, served with chutney and sambar.'},
            {'name': 'Idli', 'description': 'Steamed rice cakes, a staple breakfast item, served with coconut chutney.'},
            {'name': 'Chettinad Chicken', 'description': 'A spicy chicken curry made with aromatic spices from the Chettinad region.'},
        ]
        for cuisine in cuisines:
            Cuisine.objects.get_or_create(
                state=tamil_nadu,
                name=cuisine['name'],
                description=cuisine['description']
            )

        # Add restaurants
        restaurants = [
            {'name': 'Annalakshmi', 'specialty': 'Vegetarian South Indian', 'average_cost': 800},
            {'name': 'Ponnusamy Hotel', 'specialty': 'Chettinad Non-Veg', 'average_cost': 1000},
            {'name': 'Madras Pavilion', 'specialty': 'Multi-Cuisine', 'average_cost': 1500},
        ]
        for restaurant in restaurants:
            Restaurant.objects.get_or_create(
                state=tamil_nadu,
                name=restaurant['name'],
                specialty=restaurant['specialty'],
                average_cost=restaurant['average_cost']
            )

        # Add events
        events = [
            {'name': 'Pongal Festival', 'date': 'January 14, 2025', 'location': 'Statewide', 'description': 'A harvest festival celebrating with traditional dishes and kolam designs.'},
            {'name': 'Chithirai Festival', 'date': 'April 15, 2025', 'location': 'Madurai', 'description': 'A grand celebration at Meenakshi Temple with processions.'},
        ]
        for event in events:
            Event.objects.get_or_create(
                state=tamil_nadu,
                name=event['name'],
                date=event['date'],
                location=event['location'],
                description=event['description']
            )

        # Add itineraries
        itineraries = [
            {'day': 1, 'description': 'Arrive in Chennai, visit Marina Beach, and explore local markets.'},
            {'day': 2, 'description': 'Travel to Mahabalipuram, visit the Shore Temple, and enjoy the beach.'},
            {'day': 3, 'description': 'Head to Madurai, explore Meenakshi Temple, and attend a cultural event.'},
        ]
        for itinerary in itineraries:
            Itinerary.objects.get_or_create(
                state=tamil_nadu,
                day=itinerary['day'],
                description=itinerary['description']
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated database with Tamil Nadu data.'))