# import os
# import django
# import sys

# # Set up Django environment
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'south_india_tourism.settings')
# django.setup()

# from core.models import State, Place, Hotel

# def insert_data():
#     # Clear existing data (optional)
#     Hotel.objects.all().delete()
#     Place.objects.all().delete()
#     State.objects.all().delete()

#     # Insert States
#     kerala = State.objects.create(
#         name="Kerala",
#         description="Known for its backwaters, beaches, and lush green hills."
#     )
#     karnataka = State.objects.create(
#         name="Karnataka",
#         description="Famous for historical sites, tech hubs, and scenic landscapes."
#     )
#     tamil_nadu = State.objects.create(
#         name="Tamil Nadu",
#         description="Renowned for its ancient temples, culture, and coastal beauty."
#     )
#     andhra_pradesh = State.objects.create(
#         name="Andhra Pradesh",
#         description="Known for its rich history, temples, and cuisine."
#     )
#     telangana = State.objects.create(
#         name="Telangana",
#         description="Famous for its heritage sites, IT hubs, and unique culture."
#     )

#     # Insert Places for Kerala
#     Place.objects.create(
#         state=kerala,
#         name="Munnar",
#         category="Hill Station",
#         description="A picturesque hill station with tea plantations and misty mountains.",
#         latitude=10.0889,
#         longitude=77.0595
#     )
#     Place.objects.create(
#         state=kerala,
#         name="Alleppey",
#         category="Backwaters",
#         description="Famous for its houseboat cruises and serene backwaters.",
#         latitude=9.4981,
#         longitude=76.3388
#     )
#     Place.objects.create(
#         state=kerala,
#         name="Kochi",
#         category="Coastal",
#         description="A vibrant port city known for its Chinese fishing nets and colonial history.",
#         latitude=9.9312,
#         longitude=76.2673
#     )

#     # Insert Places for Karnataka
#     Place.objects.create(
#         state=karnataka,
#         name="Hampi",
#         category="Historical",
#         description="A UNESCO World Heritage site with ancient ruins and temples.",
#         latitude=15.3350,
#         longitude=76.4600
#     )
#     Place.objects.create(
#         state=karnataka,
#         name="Coorg",
#         category="Hill Station",
#         description="Known for coffee plantations, waterfalls, and misty hills.",
#         latitude=12.3375,
#         longitude=75.8069
#     )
#     Place.objects.create(
#         state=karnataka,
#         name="Mysore",
#         category="Cultural",
#         description="Famous for its royal heritage and the Mysore Palace.",
#         latitude=12.2958,
#         longitude=76.6394
#     )

#     # Insert Places for Tamil Nadu (Expanded with more places and coordinates)
#     Place.objects.create(
#         state=tamil_nadu,
#         name="Meenakshi Temple",
#         category="religious",
#         description="A historic Hindu temple with towering gopurams, dedicated to Goddess Meenakshi.",
#         location="Madurai",
#         latitude=9.9195,
#         longitude=78.1192,
#         entry_fee=50,
#         visiting_hours="9 AM - 7 PM",
#         safety_tip="Beware of crowded areas inside the temple."
#     )
#     Place.objects.create(
#         state=tamil_nadu,
#         name="Marina Beach",
#         category="natural",
#         description="One of the longest urban beaches in the world, perfect for a sunrise stroll.",
#         location="Chennai",
#         latitude=13.0500,
#         longitude=80.2824,
#         entry_fee=0,
#         visiting_hours="Open 24 hours",
#         safety_tip="Avoid swimming due to strong currents."
#     )
#     Place.objects.create(
#         state=tamil_nadu,
#         name="Mahabalipuram",
#         category="historical",
#         description="A UNESCO World Heritage site with ancient rock-cut temples and sculptures.",
#         location="Near Chennai",
#         latitude=12.6208,
#         longitude=80.1945,
#         entry_fee=500,
#         visiting_hours="6 AM - 6 PM",
#         safety_tip="Wear sunscreen as it can get very sunny."
#     )
#     Place.objects.create(
#         state=tamil_nadu,
#         name="Ooty",
#         category="Hill Station",
#         description="A popular hill station with lakes, gardens, and colonial charm.",
#         location="Ooty",
#         latitude=11.4102,
#         longitude=76.6950,
#         entry_fee=0,
#         visiting_hours="Open 24 hours",
#         safety_tip="Carry warm clothing for the chilly evenings."
#     )
#     Place.objects.create(
#         state=tamil_nadu,
#         name="Kanyakumari",
#         category="Coastal",
#         description="The southernmost tip of India, known for its sunrise and sunset views.",
#         location="Kanyakumari",
#         latitude=8.0883,
#         longitude=77.5385,
#         entry_fee=0,
#         visiting_hours="Open 24 hours",
#         safety_tip="Be cautious of strong waves at the beach."
#     )
#     Place.objects.create(
#         state=tamil_nadu,
#         name="Madurai",
#         category="Cultural",
#         description="Known for the Meenakshi Amman Temple and its rich history.",
#         location="Madurai",
#         latitude=9.9252,
#         longitude=78.1198,
#         entry_fee=0,
#         visiting_hours="Open 24 hours",
#         safety_tip="Follow temple etiquette when visiting religious sites."
#     )

#     # Insert Places for Andhra Pradesh
#     Place.objects.create(
#         state=andhra_pradesh,
#         name="Tirupati",
#         category="Spiritual",
#         description="Home to the famous Tirumala Venkateswara Temple.",
#         latitude=13.6288,
#         longitude=79.4192
#     )
#     Place.objects.create(
#         state=andhra_pradesh,
#         name="Araku Valley",
#         category="Hill Station",
#         description="A scenic hill station known for its coffee plantations and caves.",
#         latitude=18.3260,
#         longitude=82.8790
#     )
#     Place.objects.create(
#         state=andhra_pradesh,
#         name="Vijayawada",
#         category="Cultural",
#         description="Known for the Kanaka Durga Temple and the Krishna River.",
#         latitude=16.5062,
#         longitude=80.6480
#     )

#     # Insert Places for Telangana
#     Place.objects.create(
#         state=telangana,
#         name="Hyderabad",
#         category="Urban",
#         description="The City of Pearls, known for its Charminar and biryani.",
#         latitude=17.3850,
#         longitude=78.4867
#     )
#     Place.objects.create(
#         state=telangana,
#         name="Warangal",
#         category="Historical",
#         description="Famous for its ancient temples and the Warangal Fort.",
#         latitude=17.9784,
#         longitude=79.5941
#     )
#     Place.objects.create(
#         state=telangana,
#         name="Nizamabad",
#         category="Cultural",
#         description="Known for its historical monuments and temples.",
#         latitude=18.6720,
#         longitude=78.0941
#     )

#     # Insert Hotels for Kerala
#     Hotel.objects.create(
#         place=Place.objects.get(name="Munnar"),
#         name="Munnar Tea Resort",
#         address="Tea Valley Road, Munnar",
#         amenities="Wi-Fi, Breakfast, Spa",
#         distance=2.0
#     )
#     Hotel.objects.create(
#         place=Place.objects.get(name="Alleppey"),
#         name="Alleppey Backwater Inn",
#         address="Lake Road, Alleppey",
#         amenities="Houseboat, Wi-Fi, Breakfast",
#         distance=1.5
#     )

#     # Insert Hotels for Karnataka
#     Hotel.objects.create(
#         place=Place.objects.get(name="Hampi"),
#         name="Hampi Heritage Hotel",
#         address="Temple Road, Hampi",
#         amenities="Wi-Fi, Guided Tours, Breakfast",
#         distance=3.0
#     )
#     Hotel.objects.create(
#         place=Place.objects.get(name="Coorg"),
#         name="Coorg Coffee Estate",
#         address="Plantation Road, Coorg",
#         amenities="Nature Walks, Wi-Fi, Restaurant",
#         distance=2.8
#     )

#     # Insert Hotels for Tamil Nadu
#     Hotel.objects.create(
#         place=Place.objects.get(name="Ooty"),
#         name="Ooty Garden Resort",
#         address="Lake Road, Ooty",
#         amenities="Wi-Fi, Breakfast, Garden View",
#         distance=1.0
#     )
#     Hotel.objects.create(
#         place=Place.objects.get(name="Kanyakumari"),
#         name="Kanyakumari Sunrise Hotel",
#         address="Beach Road, Kanyakumari",
#         amenities="Sea View, Wi-Fi, Restaurant",
#         distance=0.5
#     )

#     # Insert Hotels for Andhra Pradesh
#     Hotel.objects.create(
#         place=Place.objects.get(name="Tirupati"),
#         name="Tirupati Grand Hotel",
#         address="Temple Road, Tirupati",
#         amenities="Wi-Fi, Breakfast, Parking",
#         distance=1.0
#     )
#     Hotel.objects.create(
#         place=Place.objects.get(name="Araku Valley"),
#         name="Araku Valley Resort",
#         address="Hilltop Road, Araku Valley",
#         amenities="Nature Walks, Wi-Fi, Restaurant",
#         distance=2.5
#     )

#     # Insert Hotels for Telangana
#     Hotel.objects.create(
#         place=Place.objects.get(name="Hyderabad"),
#         name="Hyderabad Pearl Hotel",
#         address="Charminar Road, Hyderabad",
#         amenities="Wi-Fi, Restaurant, Parking",
#         distance=1.0
#     )
#     Hotel.objects.create(
#         place=Place.objects.get(name="Warangal"),
#         name="Warangal Heritage Inn",
#         address="Fort Road, Warangal",
#         amenities="Wi-Fi, Breakfast, Guided Tours",
#         distance=2.0
#     )

#     print("Data inserted successfully!")

# if __name__ == "__main__":
#     insert_data()

import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'south_india_tourism.settings')
django.setup()

from core.models import State, Place

def insert_data():
    # Fetch Tamil Nadu state (do not delete existing data)
    try:
        tamil_nadu = State.objects.get(name="Tamil Nadu")
    except State.DoesNotExist:
        print("Error: Tamil Nadu state not found. Please ensure it exists in the State model.")
        return

    # Insert new places for Tamil Nadu
    places = [
        {
            'name': 'Brihadeeswarar Temple',
            'category': 'religious',
            'description': 'A UNESCO World Heritage Chola temple known for its massive gopuram and intricate stone carvings.',
            'location': 'Thanjavur',
            'latitude': 10.7828,
            'longitude': 79.1315,
            'entry_fee': 0,
            'visiting_hours': '6 AM - 12:30 PM, 4 PM - 8:30 PM',
            'safety_tip': 'Dress modestly and respect temple customs.',
            'average_rating': 4.8,
            'visit_count': 80
        },
        {
            'name': 'Ramanathaswamy Temple',
            'category': 'religious',
            'description': 'A sacred pilgrimage site with 22 holy wells and long ornate corridors, linked to the Ramayana.',
            'location': 'Rameswaram',
            'latitude': 9.2881,
            'longitude': 79.3174,
            'entry_fee': 0,
            'visiting_hours': '5 AM - 1 PM, 3 PM - 9 PM',
            'safety_tip': 'Avoid carrying leather items and follow temple rituals.',
            'average_rating': 4.7,
            'visit_count': 85
        },
        {
            'name': 'Kapaleeshwarar Temple',
            'category': 'religious',
            'description': 'A vibrant Dravidian temple dedicated to Lord Shiva, known for its colorful gopuram and festivals.',
            'location': 'Chennai',
            'latitude': 13.0334,
            'longitude': 80.2707,
            'entry_fee': 0,
            'visiting_hours': '6 AM - 1 PM, 4 PM - 9 PM',
            'safety_tip': 'Avoid visiting during peak festival times for less crowd.',
            'average_rating': 4.6,
            'visit_count': 75
        },
        {
            'name': 'Airavateswara Temple',
            'category': 'historical',
            'description': 'A UNESCO World Heritage Chola temple with exquisite carvings and architectural grandeur.',
            'location': 'Darasuram, Kumbakonam',
            'latitude': 10.9483,
            'longitude': 79.3567,
            'entry_fee': 0,
            'visiting_hours': '6 AM - 12 PM, 4 PM - 8 PM',
            'safety_tip': 'Hire a guide to appreciate the detailed carvings.',
            'average_rating': 4.7,
            'visit_count': 60
        },
        {
            'name': 'Gingee Fort',
            'category': 'historical',
            'description': 'A formidable hill fort known as the "Troy of the East," offering panoramic views and historical significance.',
            'location': 'Gingee',
            'latitude': 12.2500,
            'longitude': 79.4167,
            'entry_fee': 20,
            'visiting_hours': '9 AM - 5 PM',
            'safety_tip': 'Wear comfortable shoes for climbing the fort.',
            'average_rating': 4.4,
            'visit_count': 50
        },
        {
            'name': 'Kodaikanal',
            'category': 'Hill Station',
            'description': 'A serene hill station with lakes, waterfalls, and lush greenery, ideal for relaxation.',
            'location': 'Kodaikanal',
            'latitude': 10.2381,
            'longitude': 77.4892,
            'entry_fee': 0,
            'visiting_hours': 'Open 24 hours',
            'safety_tip': 'Carry warm clothing for cool evenings.',
            'average_rating': 4.5,
            'visit_count': 70
        },
        {
            'name': 'Yercaud',
            'category': 'Hill Station',
            'description': 'A tranquil hill station in the Eastern Ghats, known for coffee plantations and serene lakes.',
            'location': 'Salem',
            'latitude': 11.7753,
            'longitude': 78.2095,
            'entry_fee': 0,
            'visiting_hours': 'Open 24 hours',
            'safety_tip': 'Use insect repellent for outdoor activities.',
            'average_rating': 4.3,
            'visit_count': 55
        },
        {
            'name': 'Dhanushkodi Beach',
            'category': 'natural',
            'description': 'A pristine beach at a ghost town, located at the confluence of the Bay of Bengal and Indian Ocean.',
            'location': 'Rameswaram',
            'latitude': 9.1784,
            'longitude': 79.4153,
            'entry_fee': 0,
            'visiting_hours': '6 AM - 5 PM',
            'safety_tip': 'Avoid visiting after sunset due to limited facilities.',
            'average_rating': 4.5,
            'visit_count': 60
        },
        {
            'name': 'Mudumalai National Park',
            'category': 'Wildlife',
            'description': 'A biodiversity-rich national park in the Nilgiris, home to tigers, elephants, and diverse flora.',
            'location': 'Nilgiris',
            'latitude': 11.5700,
            'longitude': 76.5500,
            'entry_fee': 30,
            'visiting_hours': '6 AM - 6 PM',
            'safety_tip': 'Follow safari guidelines and avoid feeding wildlife.',
            'average_rating': 4.4,
            'visit_count': 65
        },
        {
            'name': 'Chettinad Mansions',
            'category': 'Cultural',
            'description': 'Historic mansions showcasing Chettiar architecture, known for their intricate designs and heritage.',
            'location': 'Karaikudi',
            'latitude': 10.0700,
            'longitude': 78.7800,
            'entry_fee': 100,
            'visiting_hours': '9 AM - 5 PM',
            'safety_tip': 'Respect private property and seek permission for photography.',
            'average_rating': 4.3,
            'visit_count': 50
        }
    ]

    for place_data in places:
        # Check if place already exists to avoid duplicates
        if not Place.objects.filter(state=tamil_nadu, name=place_data['name']).exists():
            Place.objects.create(
                state=tamil_nadu,
                name=place_data['name'],
                category=place_data['category'],
                description=place_data['description'],
                location=place_data['location'],
                latitude=place_data['latitude'],
                longitude=place_data['longitude'],
                entry_fee=place_data['entry_fee'],
                visiting_hours=place_data['visiting_hours'],
                safety_tip=place_data['safety_tip'],
                average_rating=place_data['average_rating'],
                visit_count=place_data['visit_count']
            )
            print(f"Inserted: {place_data['name']}")
        else:
            print(f"Skipped: {place_data['name']} already exists")

if __name__ == "__main__":
    insert_data()

