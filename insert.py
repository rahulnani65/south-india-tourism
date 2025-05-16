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
    munnar = Place.objects.create(
        state=kerala,
        name="Munnar",
        category="Hill Station",
        description="A picturesque hill station with tea plantations and misty mountains."
    )
    alleppey = Place.objects.create(
        state=kerala,
        name="Alleppey",
        category="Backwaters",
        description="Famous for its houseboat cruises and serene backwaters."
    )
    kochi = Place.objects.create(
        state=kerala,
        name="Kochi",
        category="Coastal",
        description="A vibrant port city known for its Chinese fishing nets and colonial history."
    )

    # Insert Places for Karnataka
    hampi = Place.objects.create(
        state=karnataka,
        name="Hampi",
        category="Historical",
        description="A UNESCO World Heritage site with ancient ruins and temples."
    )
    coorg = Place.objects.create(
        state=karnataka,
        name="Coorg",
        category="Hill Station",
        description="Known for coffee plantations, waterfalls, and misty hills."
    )
    mysore = Place.objects.create(
        state=karnataka,
        name="Mysore",
        category="Cultural",
        description="Famous for its royal heritage and the Mysore Palace."
    )

    # Insert Places for Tamil Nadu
    ooty = Place.objects.create(
        state=tamil_nadu,
        name="Ooty",
        category="Hill Station",
        description="A popular hill station with lakes, gardens, and colonial charm."
    )
    kanyakumari = Place.objects.create(
        state=tamil_nadu,
        name="Kanyakumari",
        category="Coastal",
        description="The southernmost tip of India, known for its sunrise and sunset views."
    )
    madurai = Place.objects.create(
        state=tamil_nadu,
        name="Madurai",
        category="Cultural",
        description="Known for the Meenakshi Amman Temple and its rich history."
    )

    # Insert Places for Andhra Pradesh
    tirupati = Place.objects.create(
        state=andhra_pradesh,
        name="Tirupati",
        category="Spiritual",
        description="Home to the famous Tirumala Venkateswara Temple."
    )
    araku_valley = Place.objects.create(
        state=andhra_pradesh,
        name="Araku Valley",
        category="Hill Station",
        description="A scenic hill station known for its coffee plantations and caves."
    )
    vijayawada = Place.objects.create(
        state=andhra_pradesh,
        name="Vijayawada",
        category="Cultural",
        description="Known for the Kanaka Durga Temple and the Krishna River."
    )

    # Insert Places for Telangana
    hyderabad = Place.objects.create(
        state=telangana,
        name="Hyderabad",
        category="Urban",
        description="The City of Pearls, known for its Charminar and biryani."
    )
    warangal = Place.objects.create(
        state=telangana,
        name="Warangal",
        category="Historical",
        description="Famous for its ancient temples and the Warangal Fort."
    )
    nizamabad = Place.objects.create(
        state=telangana,
        name="Nizamabad",
        category="Cultural",
        description="Known for its historical monuments and temples."
    )

    # Insert Hotels for Kerala
    Hotel.objects.create(
        place=munnar,
        name="Munnar Tea Resort",
        address="Tea Valley Road, Munnar",
        amenities="Wi-Fi, Breakfast, Spa",
        distance=2.0
    )
    Hotel.objects.create(
        place=alleppey,
        name="Alleppey Backwater Inn",
        address="Lake Road, Alleppey",
        amenities="Houseboat, Wi-Fi, Breakfast",
        distance=1.5
    )

    # Insert Hotels for Karnataka
    Hotel.objects.create(
        place=hampi,
        name="Hampi Heritage Hotel",
        address="Temple Road, Hampi",
        amenities="Wi-Fi, Guided Tours, Breakfast",
        distance=3.0
    )
    Hotel.objects.create(
        place=coorg,
        name="Coorg Coffee Estate",
        address="Plantation Road, Coorg",
        amenities="Nature Walks, Wi-Fi, Restaurant",
        distance=2.8
    )

    # Insert Hotels for Tamil Nadu
    Hotel.objects.create(
        place=ooty,
        name="Ooty Garden Resort",
        address="Lake Road, Ooty",
        amenities="Wi-Fi, Breakfast, Garden View",
        distance=1.0
    )
    Hotel.objects.create(
        place=kanyakumari,
        name="Kanyakumari Sunrise Hotel",
        address="Beach Road, Kanyakumari",
        amenities="Sea View, Wi-Fi, Restaurant",
        distance=0.5
    )

    # Insert Hotels for Andhra Pradesh
    Hotel.objects.create(
        place=tirupati,
        name="Tirupati Grand Hotel",
        address="Temple Road, Tirupati",
        amenities="Wi-Fi, Breakfast, Parking",
        distance=1.0
    )
    Hotel.objects.create(
        place=araku_valley,
        name="Araku Valley Resort",
        address="Hilltop Road, Araku Valley",
        amenities="Nature Walks, Wi-Fi, Restaurant",
        distance=2.5
    )

    # Insert Hotels for Telangana
    Hotel.objects.create(
        place=hyderabad,
        name="Hyderabad Pearl Hotel",
        address="Charminar Road, Hyderabad",
        amenities="Wi-Fi, Restaurant, Parking",
        distance=1.0
    )
    Hotel.objects.create(
        place=warangal,
        name="Warangal Heritage Inn",
        address="Fort Road, Warangal",
        amenities="Wi-Fi, Breakfast, Guided Tours",
        distance=2.0
    )

    print("Data inserted successfully!")

if __name__ == "__main__":
    insert_data()