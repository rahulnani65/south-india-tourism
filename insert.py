import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'south_india_tourism.settings')
django.setup()

from core.models import State, Place, Hotel

def insert_data():
    # Clear existing data (optional)
    Hotel.objects.all().delete()
    Place.objects.all().delete()
    State.objects.all().delete()

    # Insert States
    kerala = State.objects.create(
        name="Kerala",
        description="Known for its backwaters, beaches, and lush green hills."
    )
    karnataka = State.objects.create(
        name="Karnataka",
        description="Famous for historical sites, tech hubs, and scenic landscapes."
    )
    tamil_nadu = State.objects.create(
        name="Tamil Nadu",
        description="Renowned for its ancient temples, culture, and coastal beauty."
    )
    andhra_pradesh = State.objects.create(
        name="Andhra Pradesh",
        description="Known for its rich history, temples, and cuisine."
    )
    telangana = State.objects.create(
        name="Telangana",
        description="Famous for its heritage sites, IT hubs, and unique culture."
    )

    # Insert Places for Kerala
    Place.objects.create(
        state=kerala,
        name="Munnar",
        category="Hill Station",
        description="A picturesque hill station with tea plantations and misty mountains.",
        latitude=10.0889,
        longitude=77.0595
    )
    Place.objects.create(
        state=kerala,
        name="Alleppey",
        category="Backwaters",
        description="Famous for its houseboat cruises and serene backwaters.",
        latitude=9.4981,
        longitude=76.3388
    )
    Place.objects.create(
        state=kerala,
        name="Kochi",
        category="Coastal",
        description="A vibrant port city known for its Chinese fishing nets and colonial history.",
        latitude=9.9312,
        longitude=76.2673
    )

    # Insert Places for Karnataka
    Place.objects.create(
        state=karnataka,
        name="Hampi",
        category="Historical",
        description="A UNESCO World Heritage site with ancient ruins and temples.",
        latitude=15.3350,
        longitude=76.4600
    )
    Place.objects.create(
        state=karnataka,
        name="Coorg",
        category="Hill Station",
        description="Known for coffee plantations, waterfalls, and misty hills.",
        latitude=12.3375,
        longitude=75.8069
    )
    Place.objects.create(
        state=karnataka,
        name="Mysore",
        category="Cultural",
        description="Famous for its royal heritage and the Mysore Palace.",
        latitude=12.2958,
        longitude=76.6394
    )

    # Insert Places for Tamil Nadu (Expanded with more places and coordinates)
    Place.objects.create(
        state=tamil_nadu,
        name="Meenakshi Temple",
        category="religious",
        description="A historic Hindu temple with towering gopurams, dedicated to Goddess Meenakshi.",
        location="Madurai",
        latitude=9.9195,
        longitude=78.1192,
        entry_fee=50,
        visiting_hours="9 AM - 7 PM",
        safety_tip="Beware of crowded areas inside the temple."
    )
    Place.objects.create(
        state=tamil_nadu,
        name="Marina Beach",
        category="natural",
        description="One of the longest urban beaches in the world, perfect for a sunrise stroll.",
        location="Chennai",
        latitude=13.0500,
        longitude=80.2824,
        entry_fee=0,
        visiting_hours="Open 24 hours",
        safety_tip="Avoid swimming due to strong currents."
    )
    Place.objects.create(
        state=tamil_nadu,
        name="Mahabalipuram",
        category="historical",
        description="A UNESCO World Heritage site with ancient rock-cut temples and sculptures.",
        location="Near Chennai",
        latitude=12.6208,
        longitude=80.1945,
        entry_fee=500,
        visiting_hours="6 AM - 6 PM",
        safety_tip="Wear sunscreen as it can get very sunny."
    )
    Place.objects.create(
        state=tamil_nadu,
        name="Ooty",
        category="Hill Station",
        description="A popular hill station with lakes, gardens, and colonial charm.",
        location="Ooty",
        latitude=11.4102,
        longitude=76.6950,
        entry_fee=0,
        visiting_hours="Open 24 hours",
        safety_tip="Carry warm clothing for the chilly evenings."
    )
    Place.objects.create(
        state=tamil_nadu,
        name="Kanyakumari",
        category="Coastal",
        description="The southernmost tip of India, known for its sunrise and sunset views.",
        location="Kanyakumari",
        latitude=8.0883,
        longitude=77.5385,
        entry_fee=0,
        visiting_hours="Open 24 hours",
        safety_tip="Be cautious of strong waves at the beach."
    )
    Place.objects.create(
        state=tamil_nadu,
        name="Madurai",
        category="Cultural",
        description="Known for the Meenakshi Amman Temple and its rich history.",
        location="Madurai",
        latitude=9.9252,
        longitude=78.1198,
        entry_fee=0,
        visiting_hours="Open 24 hours",
        safety_tip="Follow temple etiquette when visiting religious sites."
    )

    # Insert Places for Andhra Pradesh
    Place.objects.create(
        state=andhra_pradesh,
        name="Tirupati",
        category="Spiritual",
        description="Home to the famous Tirumala Venkateswara Temple.",
        latitude=13.6288,
        longitude=79.4192
    )
    Place.objects.create(
        state=andhra_pradesh,
        name="Araku Valley",
        category="Hill Station",
        description="A scenic hill station known for its coffee plantations and caves.",
        latitude=18.3260,
        longitude=82.8790
    )
    Place.objects.create(
        state=andhra_pradesh,
        name="Vijayawada",
        category="Cultural",
        description="Known for the Kanaka Durga Temple and the Krishna River.",
        latitude=16.5062,
        longitude=80.6480
    )

    # Insert Places for Telangana
    Place.objects.create(
        state=telangana,
        name="Hyderabad",
        category="Urban",
        description="The City of Pearls, known for its Charminar and biryani.",
        latitude=17.3850,
        longitude=78.4867
    )
    Place.objects.create(
        state=telangana,
        name="Warangal",
        category="Historical",
        description="Famous for its ancient temples and the Warangal Fort.",
        latitude=17.9784,
        longitude=79.5941
    )
    Place.objects.create(
        state=telangana,
        name="Nizamabad",
        category="Cultural",
        description="Known for its historical monuments and temples.",
        latitude=18.6720,
        longitude=78.0941
    )

    # Insert Hotels for Kerala
    Hotel.objects.create(
        place=Place.objects.get(name="Munnar"),
        name="Munnar Tea Resort",
        address="Tea Valley Road, Munnar",
        amenities="Wi-Fi, Breakfast, Spa",
        distance=2.0
    )
    Hotel.objects.create(
        place=Place.objects.get(name="Alleppey"),
        name="Alleppey Backwater Inn",
        address="Lake Road, Alleppey",
        amenities="Houseboat, Wi-Fi, Breakfast",
        distance=1.5
    )

    # Insert Hotels for Karnataka
    Hotel.objects.create(
        place=Place.objects.get(name="Hampi"),
        name="Hampi Heritage Hotel",
        address="Temple Road, Hampi",
        amenities="Wi-Fi, Guided Tours, Breakfast",
        distance=3.0
    )
    Hotel.objects.create(
        place=Place.objects.get(name="Coorg"),
        name="Coorg Coffee Estate",
        address="Plantation Road, Coorg",
        amenities="Nature Walks, Wi-Fi, Restaurant",
        distance=2.8
    )

    # Insert Hotels for Tamil Nadu
    Hotel.objects.create(
        place=Place.objects.get(name="Ooty"),
        name="Ooty Garden Resort",
        address="Lake Road, Ooty",
        amenities="Wi-Fi, Breakfast, Garden View",
        distance=1.0
    )
    Hotel.objects.create(
        place=Place.objects.get(name="Kanyakumari"),
        name="Kanyakumari Sunrise Hotel",
        address="Beach Road, Kanyakumari",
        amenities="Sea View, Wi-Fi, Restaurant",
        distance=0.5
    )

    # Insert Hotels for Andhra Pradesh
    Hotel.objects.create(
        place=Place.objects.get(name="Tirupati"),
        name="Tirupati Grand Hotel",
        address="Temple Road, Tirupati",
        amenities="Wi-Fi, Breakfast, Parking",
        distance=1.0
    )
    Hotel.objects.create(
        place=Place.objects.get(name="Araku Valley"),
        name="Araku Valley Resort",
        address="Hilltop Road, Araku Valley",
        amenities="Nature Walks, Wi-Fi, Restaurant",
        distance=2.5
    )

    # Insert Hotels for Telangana
    Hotel.objects.create(
        place=Place.objects.get(name="Hyderabad"),
        name="Hyderabad Pearl Hotel",
        address="Charminar Road, Hyderabad",
        amenities="Wi-Fi, Restaurant, Parking",
        distance=1.0
    )
    Hotel.objects.create(
        place=Place.objects.get(name="Warangal"),
        name="Warangal Heritage Inn",
        address="Fort Road, Warangal",
        amenities="Wi-Fi, Breakfast, Guided Tours",
        distance=2.0
    )

    print("Data inserted successfully!")

if __name__ == "__main__":
    insert_data()