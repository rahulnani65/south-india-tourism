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

# import os
# import django
# import sys

# # Set up Django environment
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'south_india_tourism.settings')
# django.setup()

# from core.models import State, Place

# def insert_data():
#     # Fetch Tamil Nadu state (do not delete existing data)
#     try:
#         tamil_nadu = State.objects.get(name="Tamil Nadu")
#     except State.DoesNotExist:
#         print("Error: Tamil Nadu state not found. Please ensure it exists in the State model.")
#         return

#     # Insert new places for Tamil Nadu
#     places = [
#         {
#             'name': 'Brihadeeswarar Temple',
#             'category': 'religious',
#             'description': 'A UNESCO World Heritage Chola temple known for its massive gopuram and intricate stone carvings.',
#             'location': 'Thanjavur',
#             'latitude': 10.7828,
#             'longitude': 79.1315,
#             'entry_fee': 0,
#             'visiting_hours': '6 AM - 12:30 PM, 4 PM - 8:30 PM',
#             'safety_tip': 'Dress modestly and respect temple customs.',
#             'average_rating': 4.8,
#             'visit_count': 80
#         },
#         {
#             'name': 'Ramanathaswamy Temple',
#             'category': 'religious',
#             'description': 'A sacred pilgrimage site with 22 holy wells and long ornate corridors, linked to the Ramayana.',
#             'location': 'Rameswaram',
#             'latitude': 9.2881,
#             'longitude': 79.3174,
#             'entry_fee': 0,
#             'visiting_hours': '5 AM - 1 PM, 3 PM - 9 PM',
#             'safety_tip': 'Avoid carrying leather items and follow temple rituals.',
#             'average_rating': 4.7,
#             'visit_count': 85
#         },
#         {
#             'name': 'Kapaleeshwarar Temple',
#             'category': 'religious',
#             'description': 'A vibrant Dravidian temple dedicated to Lord Shiva, known for its colorful gopuram and festivals.',
#             'location': 'Chennai',
#             'latitude': 13.0334,
#             'longitude': 80.2707,
#             'entry_fee': 0,
#             'visiting_hours': '6 AM - 1 PM, 4 PM - 9 PM',
#             'safety_tip': 'Avoid visiting during peak festival times for less crowd.',
#             'average_rating': 4.6,
#             'visit_count': 75
#         },
#         {
#             'name': 'Airavateswara Temple',
#             'category': 'historical',
#             'description': 'A UNESCO World Heritage Chola temple with exquisite carvings and architectural grandeur.',
#             'location': 'Darasuram, Kumbakonam',
#             'latitude': 10.9483,
#             'longitude': 79.3567,
#             'entry_fee': 0,
#             'visiting_hours': '6 AM - 12 PM, 4 PM - 8 PM',
#             'safety_tip': 'Hire a guide to appreciate the detailed carvings.',
#             'average_rating': 4.7,
#             'visit_count': 60
#         },
#         {
#             'name': 'Gingee Fort',
#             'category': 'historical',
#             'description': 'A formidable hill fort known as the "Troy of the East," offering panoramic views and historical significance.',
#             'location': 'Gingee',
#             'latitude': 12.2500,
#             'longitude': 79.4167,
#             'entry_fee': 20,
#             'visiting_hours': '9 AM - 5 PM',
#             'safety_tip': 'Wear comfortable shoes for climbing the fort.',
#             'average_rating': 4.4,
#             'visit_count': 50
#         },
#         {
#             'name': 'Kodaikanal',
#             'category': 'Hill Station',
#             'description': 'A serene hill station with lakes, waterfalls, and lush greenery, ideal for relaxation.',
#             'location': 'Kodaikanal',
#             'latitude': 10.2381,
#             'longitude': 77.4892,
#             'entry_fee': 0,
#             'visiting_hours': 'Open 24 hours',
#             'safety_tip': 'Carry warm clothing for cool evenings.',
#             'average_rating': 4.5,
#             'visit_count': 70
#         },
#         {
#             'name': 'Yercaud',
#             'category': 'Hill Station',
#             'description': 'A tranquil hill station in the Eastern Ghats, known for coffee plantations and serene lakes.',
#             'location': 'Salem',
#             'latitude': 11.7753,
#             'longitude': 78.2095,
#             'entry_fee': 0,
#             'visiting_hours': 'Open 24 hours',
#             'safety_tip': 'Use insect repellent for outdoor activities.',
#             'average_rating': 4.3,
#             'visit_count': 55
#         },
#         {
#             'name': 'Dhanushkodi Beach',
#             'category': 'natural',
#             'description': 'A pristine beach at a ghost town, located at the confluence of the Bay of Bengal and Indian Ocean.',
#             'location': 'Rameswaram',
#             'latitude': 9.1784,
#             'longitude': 79.4153,
#             'entry_fee': 0,
#             'visiting_hours': '6 AM - 5 PM',
#             'safety_tip': 'Avoid visiting after sunset due to limited facilities.',
#             'average_rating': 4.5,
#             'visit_count': 60
#         },
#         {
#             'name': 'Mudumalai National Park',
#             'category': 'Wildlife',
#             'description': 'A biodiversity-rich national park in the Nilgiris, home to tigers, elephants, and diverse flora.',
#             'location': 'Nilgiris',
#             'latitude': 11.5700,
#             'longitude': 76.5500,
#             'entry_fee': 30,
#             'visiting_hours': '6 AM - 6 PM',
#             'safety_tip': 'Follow safari guidelines and avoid feeding wildlife.',
#             'average_rating': 4.4,
#             'visit_count': 65
#         },
#         {
#             'name': 'Chettinad Mansions',
#             'category': 'Cultural',
#             'description': 'Historic mansions showcasing Chettiar architecture, known for their intricate designs and heritage.',
#             'location': 'Karaikudi',
#             'latitude': 10.0700,
#             'longitude': 78.7800,
#             'entry_fee': 100,
#             'visiting_hours': '9 AM - 5 PM',
#             'safety_tip': 'Respect private property and seek permission for photography.',
#             'average_rating': 4.3,
#             'visit_count': 50
#         }
#     ]

#     for place_data in places:
#         # Check if place already exists to avoid duplicates
#         if not Place.objects.filter(state=tamil_nadu, name=place_data['name']).exists():
#             Place.objects.create(
#                 state=tamil_nadu,
#                 name=place_data['name'],
#                 category=place_data['category'],
#                 description=place_data['description'],
#                 location=place_data['location'],
#                 latitude=place_data['latitude'],
#                 longitude=place_data['longitude'],
#                 entry_fee=place_data['entry_fee'],
#                 visiting_hours=place_data['visiting_hours'],
#                 safety_tip=place_data['safety_tip'],
#                 average_rating=place_data['average_rating'],
#                 visit_count=place_data['visit_count']
#             )
#             print(f"Inserted: {place_data['name']}")
#         else:
#             print(f"Skipped: {place_data['name']} already exists")

# if __name__ == "__main__":
#     insert_data()




# import os
# import django
# import sys

# # Set up Django environment
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'south_india_tourism.settings')
# django.setup()

# from core.models import State, Place

# def insert_data():
#     # Fetch Telangana state (do not delete existing data)
#     try:
#         telangana = State.objects.get(name="Telangana")
#     except State.DoesNotExist:
#         print("Error: Telangana state not found. Please ensure it exists in the State model.")
#         return

#     # Insert new places for Telangana
#     places = [
#         {
#             'name': 'Bhadrachalam Temple',
#             'category': 'religious',
#             'description': 'A revered temple on the Godavari River dedicated to Lord Rama, known for its vibrant festivals.',
#             'location': 'Bhadrachalam',
#             'latitude': 17.6688,
#             'longitude': 80.8937,
#             'entry_fee': 0.00,
#             'visiting_hours': '4:30 AM - 12 PM, 3 PM - 8:30 PM',
#             'safety_tip': 'Dress modestly and avoid visiting during peak festival times.',
#             'average_rating': 4.7,
#             'visit_count': 90
#         },
#         {
#             'name': 'Yadagirigutta Temple',
#             'category': 'religious',
#             'description': 'A major pilgrimage site dedicated to Lord Narasimha, set on a hill with stunning architecture.',
#             'location': 'Yadagirigutta',
#             'latitude': 17.5841,
#             'longitude': 78.9438,
#             'entry_fee': 0.00,
#             'visiting_hours': '4 AM - 10 PM',
#             'safety_tip': 'Watch for slippery steps during monsoon season.',
#             'average_rating': 4.6,
#             'visit_count': 85
#         },
#         {
#             'name': 'Thousand Pillar Temple',
#             'category': 'historical',
#             'description': 'A 12th-century Kakatiya temple in Hanamkonda, famous for its intricate carvings and pillars.',
#             'location': 'Hanamkonda',
#             'latitude': 18.0057,
#             'longitude': 79.5741,
#             'entry_fee': 0.00,
#             'visiting_hours': '6 AM - 8 PM',
#             'safety_tip': 'Hire a guide to learn about the temple’s historical details.',
#             'average_rating': 4.8,
#             'visit_count': 70
#         },
#         {
#             'name': 'Bhongir Fort',
#             'category': 'historical',
#             'description': 'A unique egg-shaped hill fort from the 10th century, offering panoramic views and adventure.',
#             'location': 'Bhongir',
#             'latitude': 17.5108,
#             'longitude': 78.8889,
#             'entry_fee': 10.00,
#             'visiting_hours': '10 AM - 5 PM',
#             'safety_tip': 'Wear comfortable shoes for the steep climb.',
#             'average_rating': 4.4,
#             'visit_count': 60
#         },
#         {
#             'name': 'Kuntala Waterfall',
#             'category': 'natural',
#             'description': 'Telangana’s highest waterfall, surrounded by dense forests, ideal for nature lovers and picnics.',
#             'location': 'Adilabad',
#             'latitude': 19.3833,
#             'longitude': 78.4667,
#             'entry_fee': 20.00,
#             'visiting_hours': '8 AM - 5 PM',
#             'safety_tip': 'Avoid swimming in deep areas due to strong currents.',
#             'average_rating': 4.5,
#             'visit_count': 65
#         },
#         {
#             'name': 'Pakhal Lake',
#             'category': 'natural',
#             'description': 'A serene man-made lake amidst forests, perfect for boating and peaceful retreats.',
#             'location': 'Warangal',
#             'latitude': 17.9486,
#             'longitude': 79.8425,
#             'entry_fee': 30.00,
#             'visiting_hours': '9 AM - 6 PM',
#             'safety_tip': 'Use authorized boats for safe boating experiences.',
#             'average_rating': 4.3,
#             'visit_count': 55
#         },
#         {
#             'name': 'Ramoji Film City',
#             'category': 'cultural',
#             'description': 'The world’s largest film studio, offering tours, live shows, and a glimpse into Indian cinema.',
#             'location': 'Hyderabad',
#             'latitude': 17.2568,
#             'longitude': 78.6814,
#             'entry_fee': 1350.00,
#             'visiting_hours': '9 AM - 5:30 PM',
#             'safety_tip': 'Book tickets online to avoid long queues.',
#             'average_rating': 4.6,
#             'visit_count': 100
#         },
#         {
#             'name': 'Kala Ashram',
#             'category': 'cultural',
#             'description': 'A cultural center in Adilabad promoting traditional arts, crafts, and tribal performances.',
#             'location': 'Adilabad',
#             'latitude': 19.6760,
#             'longitude': 78.5290,
#             'entry_fee': 50.00,
#             'visiting_hours': '10 AM - 6 PM',
#             'safety_tip': 'Respect ongoing workshops and seek permission for photography.',
#             'average_rating': 4.2,
#             'visit_count': 50
#         },
#         {
#             'name': 'Kawal Wildlife Sanctuary',
#             'category': 'Wildlife',
#             'description': 'A tiger reserve with rich biodiversity, home to tigers, leopards, and diverse bird species.',
#             'location': 'Adilabad',
#             'latitude': 19.1667,
#             'longitude': 78.6667,
#             'entry_fee': 50.00,
#             'visiting_hours': '6 AM - 6 PM',
#             'safety_tip': 'Follow safari guidelines and avoid disturbing wildlife.',
#             'average_rating': 4.4,
#             'visit_count': 60
#         },
#         {
#             'name': 'Pocharam Wildlife Sanctuary',
#             'category': 'Wildlife',
#             'description': 'A scenic sanctuary near Medak with deer, birds, and a tranquil lake, ideal for nature walks.',
#             'location': 'Medak',
#             'latitude': 18.1350,
#             'longitude': 78.3550,
#             'entry_fee': 30.00,
#             'visiting_hours': '8 AM - 5 PM',
#             'safety_tip': 'Carry binoculars for birdwatching and stay on designated paths.',
#             'average_rating': 4.3,
#             'visit_count': 55
#         },
#         {
#             'name': 'Medak Cathedral',
#             'category': 'historical',
#             'description': 'A grand Gothic-style church, one of the largest in Asia, known for its stained glass windows.',
#             'location': 'Medak',
#             'latitude': 18.0459,
#             'longitude': 78.2639,
#             'entry_fee': 0.00,
#             'visiting_hours': '9 AM - 5 PM',
#             'safety_tip': 'Maintain silence and respect religious services.',
#             'average_rating': 4.5,
#             'visit_count': 70
#         },
#         {
#             'name': 'Ananthagiri Hills',
#             'category': 'natural',
#             'description': 'A scenic hill station near Hyderabad, known for trekking, coffee plantations, and lush greenery.',
#             'location': 'Vikarabad',
#             'latitude': 17.2833,
#             'longitude': 77.8167,
#             'entry_fee': 0.00,
#             'visiting_hours': 'Open 24 hours',
#             'safety_tip': 'Hire a local guide for safe trekking routes.',
#             'average_rating': 4.4,
#             'visit_count': 60
#         },
#         {
#             'name': 'Sammakka Saralamma Jatara',
#             'category': 'cultural',
#             'description': 'A major tribal festival in Medaram, one of the largest in India, celebrating tribal deities.',
#             'location': 'Medaram',
#             'latitude': 18.3833,
#             'longitude': 80.0167,
#             'entry_fee': 0.00,
#             'visiting_hours': 'Festival-specific, check schedule',
#             'safety_tip': 'Plan for large crowds during the biennial festival.',
#             'average_rating': 4.6,
#             'visit_count': 80
#         },
#         {
#             'name': 'Ramappa Temple',
#             'category': 'historical',
#             'description': 'A UNESCO World Heritage Kakatiya temple known for its floating bricks and intricate sculptures.',
#             'location': 'Mulugu',
#             'latitude': 18.2593,
#             'longitude': 79.9402,
#             'entry_fee': 25.00,
#             'visiting_hours': '6 AM - 6 PM',
#             'safety_tip': 'Protect against sun exposure during daytime visits.',
#             'average_rating': 4.8,
#             'visit_count': 75
#         },
#         {
#             'name': 'Laknavaram Lake',
#             'category': 'natural',
#             'description': 'A picturesque lake with a suspension bridge and islands, ideal for boating and camping.',
#             'location': 'Mulugu',
#             'latitude': 18.3167,
#             'longitude': 80.1167,
#             'entry_fee': 20.00,
#             'visiting_hours': '9 AM - 6 PM',
#             'safety_tip': 'Ensure life jackets are worn during boating.',
#             'average_rating': 4.5,
#             'visit_count': 65
#         }
#     ]

#     for place_data in places:
#         # Check if place already exists to avoid duplicates
#         if not Place.objects.filter(state=telangana, name=place_data['name']).exists():
#             Place.objects.create(
#                 state=telangana,
#                 name=place_data['name'],
#                 category=place_data['category'],
#                 description=place_data['description'],
#                 location=place_data['location'],
#                 latitude=place_data['latitude'],
#                 longitude=place_data['longitude'],
#                 entry_fee=place_data['entry_fee'],
#                 visiting_hours=place_data['visiting_hours'],
#                 safety_tip=place_data['safety_tip'],
#                 average_rating=place_data['average_rating'],
#                 visit_count=place_data['visit_count']
#             )
#             print(f"Inserted: {place_data['name']}")
#         else:
#             print(f"Skipped: {place_data['name']} already exists")

# if __name__ == "__main__":
#     insert_data()

# import os
# import django
# import sys

# # Set up Django environment
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'south_india_tourism.settings')
# django.setup()

# from core.models import State, Place

# def insert_data():
#     # Fetch Karnataka state (do not delete existing data)
#     try:
#         karnataka = State.objects.get(name="Karnataka")
#     except State.DoesNotExist:
#         print("Error: Karnataka state not found. Please ensure it exists in the State model.")
#         return

#     # Insert places for Karnataka (15 previous + 10 new)
#     places = [
#         # Previous 15 places
#         {
#             'name': 'Badami Cave Temples',
#             'category': 'historical',
#             'description': 'A complex of rock-cut temples from the 6th century, showcasing Chalukya architecture.',
#             'location': 'Badami',
#             'latitude': 15.9187,
#             'longitude': 75.6850,
#             'entry_fee': 30.00,
#             'visiting_hours': '9 AM - 5:30 PM',
#             'safety_tip': 'Wear comfortable shoes for exploring the caves.',
#             'average_rating': 4.7,
#             'visit_count': 70
#         },
#         {
#             'name': 'Sringeri Sharada Peetham',
#             'category': 'religious',
#             'description': 'A historic Advaita Vedanta monastery founded by Adi Shankaracharya, set by the Tunga River.',
#             'location': 'Sringeri',
#             'latitude': 13.4167,
#             'longitude': 75.2520,
#             'entry_fee': 0.00,
#             'visiting_hours': '6 AM - 2 PM, 4 PM - 9 PM',
#             'safety_tip': 'Dress modestly and respect temple rituals.',
#             'average_rating': 4.8,
#             'visit_count': 85
#         },
#         {
#             'name': 'Jog Falls',
#             'category': 'natural',
#             'description': 'India’s second-highest waterfall, offering spectacular views amidst lush greenery.',
#             'location': 'Shimoga',
#             'latitude': 14.2293,
#             'longitude': 74.8124,
#             'entry_fee': 20.00,
#             'visiting_hours': '7:30 AM - 6 PM',
#             'safety_tip': 'Avoid getting too close to the edge of viewpoints.',
#             'average_rating': 4.6,
#             'visit_count': 80
#         },
#         {
#             'name': 'Belur Halebidu Temples',
#             'category': 'historical',
#             'description': 'Hoysala-era temples known for their intricate stone carvings and architectural brilliance.',
#             'location': 'Hassan',
#             'latitude': 13.1625,
#             'longitude': 75.8600,
#             'entry_fee': 0.00,
#             'visiting_hours': '7 AM - 6 PM',
#             'safety_tip': 'Hire a guide to understand the detailed carvings.',
#             'average_rating': 4.8,
#             'visit_count': 75
#         },
#         {
#             'name': 'Chikmagalur',
#             'category': 'Hill Station',
#             'description': 'A serene hill station known for coffee plantations, trekking, and Mullayanagiri peak.',
#             'location': 'Chikmagalur',
#             'latitude': 13.3167,
#             'longitude': 75.7833,
#             'entry_fee': 0.00,
#             'visiting_hours': 'Open 24 hours',
#             'safety_tip': 'Carry warm clothing for early morning treks.',
#             'average_rating': 4.5,
#             'visit_count': 65
#         },
#         {
#             'name': 'Dandeli Wildlife Sanctuary',
#             'category': 'Wildlife',
#             'description': 'A biodiversity hotspot offering jungle safaris, river rafting, and sightings of hornbills and leopards.',
#             'location': 'Dandeli',
#             'latitude': 15.2667,
#             'longitude': 74.6167,
#             'entry_fee': 50.00,
#             'visiting_hours': '6 AM - 6 PM',
#             'safety_tip': 'Follow guide instructions during safaris and rafting.',
#             'average_rating': 4.4,
#             'visit_count': 60
#         },
#         {
#             'name': 'Udupi Sri Krishna Temple',
#             'category': 'religious',
#             'description': 'A famous temple known for its unique idol of Lord Krishna and vibrant festivals.',
#             'location': 'Udupi',
#             'latitude': 13.3388,
#             'longitude': 74.7461,
#             'entry_fee': 0.00,
#             'visiting_hours': '4 AM - 9 PM',
#             'safety_tip': 'Avoid peak hours for a peaceful visit.',
#             'average_rating': 4.7,
#             'visit_count': 90
#         },
#         {
#             'name': 'Gokarna Beach',
#             'category': 'natural',
#             'description': 'A pristine beach known for its serene vibe, pilgrimage sites, and water activities.',
#             'location': 'Gokarna',
#             'latitude': 14.5500,
#             'longitude': 74.3167,
#             'entry_fee': 0.00,
#             'visiting_hours': 'Open 24 hours',
#             'safety_tip': 'Avoid swimming during high tides.',
#             'average_rating': 4.5,
#             'visit_count': 70
#         },
#         {
#             'name': 'Bannerghatta National Park',
#             'category': 'Wildlife',
#             'description': 'A popular park near Bangalore with a zoo, safari, and butterfly park.',
#             'location': 'Bangalore',
#             'latitude': 12.8000,
#             'longitude': 77.5833,
#             'entry_fee': 80.00,
#             'visiting_hours': '9:30 AM - 5 PM',
#             'safety_tip': 'Stay inside vehicles during the safari.',
#             'average_rating': 4.3,
#             'visit_count': 100
#         },
#         {
#             'name': 'Nandi Hills',
#             'category': 'natural',
#             'description': 'A popular hill fortress near Bangalore, famous for sunrise views and paragliding.',
#             'location': 'Chikkaballapur',
#             'latitude': 13.3700,
#             'longitude': 77.6833,
#             'entry_fee': 30.00,
#             'visiting_hours': '6 AM - 10 PM',
#             'safety_tip': 'Arrive early to avoid crowds at sunrise.',
#             'average_rating': 4.4,
#             'visit_count': 85
#         },
#         {
#             'name': 'Shravanabelagola',
#             'category': 'religious',
#             'description': 'A Jain pilgrimage site with the colossal Gommateshwara Bahubali statue atop a hill.',
#             'location': 'Hassan',
#             'latitude': 12.8540,
#             'longitude': 76.4849,
#             'entry_fee': 0.00,
#             'visiting_hours': '6:30 AM - 6 PM',
#             'safety_tip': 'Climb the 600+ steps carefully, preferably early morning.',
#             'average_rating': 4.7,
#             'visit_count': 80
#         },
#         {
#             'name': 'Vidhana Soudha',
#             'category': 'cultural',
#             'description': 'The majestic seat of Karnataka’s state legislature, known for its neo-Dravidian architecture.',
#             'location': 'Bangalore',
#             'latitude': 12.9795,
#             'longitude': 77.5916,
#             'entry_fee': 0.00,
#             'visiting_hours': '9 AM - 5 PM (public access limited)',
#             'safety_tip': 'Carry ID for entry and avoid restricted areas.',
#             'average_rating': 4.5,
#             'visit_count': 90
#         },
#         {
#             'name': 'Murudeshwar Temple',
#             'category': 'religious',
#             'description': 'A coastal temple with a towering Shiva statue and a 20-story gopuram, offering sea views.',
#             'location': 'Murudeshwar',
#             'latitude': 14.0943,
#             'longitude': 74.4845,
#             'entry_fee': 0.00,
#             'visiting_hours': '6 AM - 8 PM',
#             'safety_tip': 'Be cautious on the gopuram stairs during windy conditions.',
#             'average_rating': 4.6,
#             'visit_count': 75
#         },
#         {
#             'name': 'Aihole',
#             'category': 'historical',
#             'description': 'An ancient site with over 100 Chalukya temples, known as the cradle of Indian temple architecture.',
#             'location': 'Bagalkot',
#             'latitude': 16.0200,
#             'longitude': 75.8833,
#             'entry_fee': 25.00,
#             'visiting_hours': '6 AM - 6 PM',
#             'safety_tip': 'Carry water as the site is expansive and sunny.',
#             'average_rating': 4.6,
#             'visit_count': 60
#         },
#         {
#             'name': 'Kudremukh National Park',
#             'category': 'Wildlife',
#             'description': 'A UNESCO World Heritage biodiversity hotspot with trekking trails and scenic peaks.',
#             'location': 'Chikmagalur',
#             'latitude': 13.2333,
#             'longitude': 75.1667,
#             'entry_fee': 200.00,
#             'visiting_hours': '7 AM - 5 PM',
#             'safety_tip': 'Obtain permits in advance for trekking.',
#             'average_rating': 4.5,
#             'visit_count': 55
#         },
#         # New 10 popular places
#         {
#             'name': 'Pattadakal',
#             'category': 'historical',
#             'description': 'A UNESCO World Heritage site with 8th-century Chalukya temples, known for their architectural diversity.',
#             'location': 'Bagalkot',
#             'latitude': 15.9480,
#             'longitude': 75.8160,
#             'entry_fee': 40.00,
#             'visiting_hours': '6 AM - 6 PM',
#             'safety_tip': 'Protect against sun exposure during daytime visits.',
#             'average_rating': 4.7,
#             'visit_count': 65
#         },
#         {
#             'name': 'Dharmasthala Manjunatha Temple',
#             'category': 'religious',
#             'description': 'A major pilgrimage site dedicated to Lord Shiva, known for its inclusive ethos and free meals.',
#             'location': 'Dharmasthala',
#             'latitude': 12.8928,
#             'longitude': 75.3789,
#             'entry_fee': 0.00,
#             'visiting_hours': '6:30 AM - 8:30 PM',
#             'safety_tip': 'Follow queue systems during peak pilgrimage seasons.',
#             'average_rating': 4.8,
#             'visit_count': 95
#         },
#         {
#             'name': 'Agumbe Rainforest',
#             'category': 'natural',
#             'description': 'A biodiversity-rich rainforest, known as the ‘Cherrapunji of the South,’ ideal for trekking and sunset views.',
#             'location': 'Shimoga',
#             'latitude': 13.5033,
#             'longitude': 75.0917,
#             'entry_fee': 0.00,
#             'visiting_hours': 'Open 24 hours',
#             'safety_tip': 'Hire a local guide for safe trekking in the rainforest.',
#             'average_rating': 4.5,
#             'visit_count': 60
#         },
#         {
#             'name': 'Bijapur Gol Gumbaz',
#             'category': 'historical',
#             'description': 'A 17th-century mausoleum with one of the world’s largest domes and a whispering gallery.',
#             'location': 'Bijapur',
#             'latitude': 16.8302,
#             'longitude': 75.7350,
#             'entry_fee': 25.00,
#             'visiting_hours': '10 AM - 5 PM',
#             'safety_tip': 'Be cautious on the narrow stairs to the whispering gallery.',
#             'average_rating': 4.6,
#             'visit_count': 70
#         },
#         {
#             'name': 'Kabini Wildlife Sanctuary',
#             'category': 'Wildlife',
#             'description': 'A premier wildlife destination with elephant safaris, tiger sightings, and serene river views.',
#             'location': 'Nagarhole',
#             'latitude': 11.9833,
#             'longitude': 76.2833,
#             'entry_fee': 300.00,
#             'visiting_hours': '6 AM - 6 PM',
#             'safety_tip': 'Book safaris in advance and follow guide instructions.',
#             'average_rating': 4.7,
#             'visit_count': 80
#         },
#         {
#             'name': 'Kollur Mookambika Temple',
#             'category': 'religious',
#             'description': 'A sacred temple in the Western Ghats dedicated to Goddess Mookambika, known for its spiritual ambiance.',
#             'location': 'Kollur',
#             'latitude': 13.8633,
#             'longitude': 74.8144,
#             'entry_fee': 0.00,
#             'visiting_hours': '5 AM - 9 PM',
#             'safety_tip': 'Respect temple customs and avoid photography inside.',
#             'average_rating': 4.7,
#             'visit_count': 85
#         },
#         {
#             'name': 'Karwar Beach',
#             'category': 'natural',
#             'description': 'A tranquil beach along the Arabian Sea, known for water sports and scenic beauty.',
#             'location': 'Karwar',
#             'latitude': 14.8183,
#             'longitude': 74.1297,
#             'entry_fee': 0.00,
#             'visiting_hours': 'Open 24 hours',
#             'safety_tip': 'Check tide schedules before engaging in water activities.',
#             'average_rating': 4.4,
#             'visit_count': 65
#         },
#         {
#             'name': 'Lalbagh Botanical Garden',
#             'category': 'cultural',
#             'description': 'A historic garden in Bangalore with rare plants, a glasshouse, and vibrant flower shows.',
#             'location': 'Bangalore',
#             'latitude': 12.9507,
#             'longitude': 77.5848,
#             'entry_fee': 20.00,
#             'visiting_hours': '6 AM - 7 PM',
#             'safety_tip': 'Avoid visiting during peak flower show crowds.',
#             'average_rating': 4.5,
#             'visit_count': 95
#         },
#         {
#             'name': 'Sakleshpur',
#             'category': 'Hill Station',
#             'description': 'A picturesque hill station with coffee estates, trekking trails, and historic Manjarabad Fort.',
#             'location': 'Hassan',
#             'latitude': 12.9417,
#             'longitude': 75.7833,
#             'entry_fee': 0.00,
#             'visiting_hours': 'Open 24 hours',
#             'safety_tip': 'Carry insect repellent for outdoor activities.',
#             'average_rating': 4.4,
#             'visit_count': 60
#         },
#         {
#             'name': 'Bandipur National Park',
#             'category': 'Wildlife',
#             'description': 'A renowned tiger reserve with rich biodiversity, offering safaris and scenic drives.',
#             'location': 'Chamarajanagar',
#             'latitude': 11.6670,
#             'longitude': 76.6330,
#             'entry_fee': 250.00,
#             'visiting_hours': '6 AM - 6 PM',
#             'safety_tip': 'Stay inside vehicles and avoid loud noises during safaris.',
#             'average_rating': 4.6,
#             'visit_count': 75
#         }
#     ]

#     for place_data in places:
#         # Check if place already exists to avoid duplicates
#         if not Place.objects.filter(state=karnataka, name=place_data['name']).exists():
#             Place.objects.create(
#                 state=karnataka,
#                 name=place_data['name'],
#                 category=place_data['category'],
#                 description=place_data['description'],
#                 location=place_data['location'],
#                 latitude=place_data['latitude'],
#                 longitude=place_data['longitude'],
#                 entry_fee=place_data['entry_fee'],
#                 visiting_hours=place_data['visiting_hours'],
#                 safety_tip=place_data['safety_tip'],
#                 average_rating=place_data['average_rating'],
#                 visit_count=place_data['visit_count']
#             )
#             print(f"Inserted: {place_data['name']}")
#         else:
#             print(f"Skipped: {place_data['name']} already exists")

# if __name__ == "__main__":
#     insert_data()


# import os
# import django
# import sys

# # Set up Django environment
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'south_india_tourism.settings')
# django.setup()

# from core.models import State

# def populate_state_data():
#     # Define data for each state (excluding Tamil Nadu)
#     state_data = [
#         {
#             'id': 1,
#             'name': 'Kerala',
#             'slug': 'kerala',
#             'description': 'Known for its backwaters, beaches, and lush green hills.',
#             'history': 'Kerala has a rich history dating back to the Sangam Age, with influences from trade with Arabs, Chinese, and Europeans.',
#             'culture': 'Famous for Kathakali dance, Ayurvedic traditions, and Onam festival.',
#             'climate': 'Tropical with monsoon seasons; hot and humid summers, mild winters.',
#             'best_time_to_visit': 'September to March',
#             'cultural_safety_tips': [
#                 'Respect local customs during temple visits.',
#                 'Avoid public displays of affection in rural areas.',
#                 'Use authorized boat services for backwater tours.'
#             ]
#         },
#         {
#             'id': 2,
#             'name': 'Karnataka',
#             'slug': 'karnataka',
#             'description': 'Famous for historical sites, tech hubs, and scenic landscapes.',
#             'history': 'Karnataka was ruled by dynasties like the Chalukyas, Hoysalas, and Vijayanagara Empire, shaping its rich heritage.',
#             'culture': 'Known for Carnatic music, Udupi cuisine, and Mysore Dasara festival.',
#             'climate': 'Tropical with varied climates; cooler in hills, hot in plains.',
#             'best_time_to_visit': 'October to March',
#             'cultural_safety_tips': [
#                 'Dress modestly at religious sites.',
#                 'Respect local wildlife during park visits.',
#                 'Avoid photography in restricted temple areas.'
#             ]
#         },
#         {
#             'id': 4,
#             'name': 'Andhra Pradesh',
#             'slug': 'andhra-pradesh',
#             'description': 'Known for its rich history, temples, and cuisine.',
#             'history': 'Influenced by the Satavahanas, Vijayanagara, and British rule, with a legacy of ancient trade.',
#             'culture': 'Famous for Kuchipudi dance, Telugu literature, and Ugadi festival.',
#             'climate': 'Tropical with hot summers and monsoon rains.',
#             'best_time_to_visit': 'October to February',
#             'cultural_safety_tips': [
#                 'Follow temple dress codes and remove footwear.',
#                 'Avoid crowded areas during festivals.',
#                 'Use licensed guides for historical sites.'
#             ]
#         },
#         {
#             'id': 5,
#             'name': 'Telangana',
#             'slug': 'telangana',
#             'description': 'Famous for its heritage sites, IT hubs, and unique culture.',
#             'history': 'Part of the Hyderabad State under the Nizams, with a legacy of Qutb Shahi and Asaf Jahi dynasties.',
#             'culture': 'Known for Bonalu festival, Hyderabadi biryani, and traditional crafts.',
#             'climate': 'Tropical with hot summers and moderate monsoons.',
#             'best_time_to_visit': 'October to March',
#             'cultural_safety_tips': [
#                 'Respect temple and festival customs.',
#                 'Avoid swimming in unknown water bodies near waterfalls.',
#                 'Seek permission for photography at cultural sites.'
#             ]
#         }
#     ]

#     for state in state_data:
#         # Update or create state record
#         state_obj, created = State.objects.update_or_create(
#             id=state['id'],
#             defaults={
#                 'name': state['name'],
#                 'slug': state['slug'],
#                 'description': state['description'],
#                 'history': state['history'],
#                 'culture': state['culture'],
#                 'climate': state['climate'],
#                 'best_time_to_visit': state['best_time_to_visit'],
#                 'cultural_safety_tips': state['cultural_safety_tips']
#             }
#         )
#         if created:
#             print(f"Created: {state['name']}")
#         else:
#             print(f"Updated: {state['name']}")

# if __name__ == "__main__":
#     populate_state_data()



# import os
# import django
# import sys

# # Set up Django environment
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'south_india_tourism.settings')
# django.setup()

# from core.models import State, Place

# def insert_data():
#     # Fetch Andhra Pradesh state (do not delete existing data)
#     try:
#         andhra_pradesh = State.objects.get(name="Andhra Pradesh")
#     except State.DoesNotExist:
#         print("Error: Andhra Pradesh state not found. Please ensure it exists in the State model.")
#         return

#     # Insert new places for Andhra Pradesh
#     places = [
#         {
#             'name': 'Srisailam Temple',
#             'category': 'religious',
#             'description': 'A sacred Jyotirlinga temple dedicated to Lord Shiva, nestled in the Nallamala Hills.',
#             'location': 'Srisailam',
#             'latitude': 16.0760,
#             'longitude': 78.8700,
#             'entry_fee': 0.00,
#             'visiting_hours': '6 AM - 2 PM, 3 PM - 10 PM',
#             'safety_tip': 'Follow temple dress codes and avoid peak pilgrimage times.',
#             'average_rating': 4.7,
#             'visit_count': 85
#         },
#         {
#             'name': 'Visakhapatnam Beach',
#             'category': 'natural',
#             'description': 'A scenic coastline with popular beaches like RK Beach, ideal for strolls and water sports.',
#             'location': 'Visakhapatnam',
#             'latitude': 17.6868,
#             'longitude': 83.2185,
#             'entry_fee': 0.00,
#             'visiting_hours': 'Open 24 hours',
#             'safety_tip': 'Avoid swimming in deep waters due to strong currents.',
#             'average_rating': 4.5,
#             'visit_count': 90
#         },
#         {
#             'name': 'Amaravati Stupa',
#             'category': 'historical',
#             'description': 'An ancient Buddhist site with a massive stupa, reflecting the region’s rich Buddhist heritage.',
#             'location': 'Amaravati',
#             'latitude': 16.5750,
#             'longitude': 80.3550,
#             'entry_fee': 10.00,
#             'visiting_hours': '8 AM - 6 PM',
#             'safety_tip': 'Wear sunscreen and hats during sunny hours.',
#             'average_rating': 4.6,
#             'visit_count': 70
#         },
#         {
#             'name': 'Lambasingi',
#             'category': 'Hill Station',
#             'description': 'Known as the "Kashmir of Andhra," this hill station offers cool weather and scenic views.',
#             'location': 'Visakhapatnam',
#             'latitude': 18.1690,
#             'longitude': 82.6560,
#             'entry_fee': 0.00,
#             'visiting_hours': 'Open 24 hours',
#             'safety_tip': 'Carry warm clothing for chilly evenings.',
#             'average_rating': 4.4,
#             'visit_count': 60
#         },
#         {
#             'name': 'Ahobilam Temple',
#             'category': 'religious',
#             'description': 'A group of nine temples dedicated to Lord Narasimha, located in the Nallamala Forest.',
#             'location': 'Ahobilam',
#             'latitude': 15.1250,
#             'longitude': 78.7167,
#             'entry_fee': 0.00,
#             'visiting_hours': '6 AM - 1 PM, 3 PM - 8 PM',
#             'safety_tip': 'Hire a local guide for safe trekking to the temples.',
#             'average_rating': 4.7,
#             'visit_count': 75
#         },
#         {
#             'name': 'Kailasagiri Hill',
#             'category': 'natural',
#             'description': 'A scenic hill park in Visakhapatnam with panoramic views, a toy train, and Shiva-Parvati statues.',
#             'location': 'Visakhapatnam',
#             'latitude': 17.7510,
#             'longitude': 83.3410,
#             'entry_fee': 0.00,
#             'visiting_hours': '6 AM - 7:30 PM',
#             'safety_tip': 'Stay on designated paths to avoid steep drops.',
#             'average_rating': 4.5,
#             'visit_count': 85
#         },
#         {
#             'name': 'Guntur Fort',
#             'category': 'historical',
#             'description': 'A 19th-century fort with historical significance, offering insights into the region’s past.',
#             'location': 'Guntur',
#             'latitude': 16.3067,
#             'longitude': 80.4367,
#             'entry_fee': 5.00,
#             'visiting_hours': '9 AM - 5 PM',
#             'safety_tip': 'Be cautious of uneven surfaces while exploring.',
#             'average_rating': 4.3,
#             'visit_count': 55
#         },
#         {
#             'name': 'Konaseema',
#             'category': 'natural',
#             'description': 'A picturesque delta region with lush greenery, rivers, and backwaters, often called the "God’s Own Creation."',
#             'location': 'East Godavari',
#             'latitude': 16.7333,
#             'longitude': 81.9167,
#             'entry_fee': 0.00,
#             'visiting_hours': 'Open 24 hours',
#             'safety_tip': 'Use authorized boat operators for safety.',
#             'average_rating': 4.6,
#             'visit_count': 70
#         },
#         {
#             'name': 'Simhachalam Temple',
#             'category': 'religious',
#             'description': 'A hilltop temple dedicated to Lord Varaha Narasimha, known for its ancient architecture.',
#             'location': 'Visakhapatnam',
#             'latitude': 17.7760,
#             'longitude': 83.2390,
#             'entry_fee': 0.00,
#             'visiting_hours': '7 AM - 4 PM, 6 PM - 9 PM',
#             'safety_tip': 'Climb the steps cautiously, especially during rains.',
#             'average_rating': 4.7,
#             'visit_count': 80
#         },
#         {
#             'name': 'Kondapalli Fort',
#             'category': 'historical',
#             'description': 'A 14th-century fort known for its scenic location and historical importance.',
#             'location': 'Kondapalli',
#             'latitude': 16.6167,
#             'longitude': 80.5333,
#             'entry_fee': 10.00,
#             'visiting_hours': '8 AM - 5 PM',
#             'safety_tip': 'Wear sturdy shoes for the uphill trek.',
#             'average_rating': 4.4,
#             'visit_count': 60
#         },
#         {
#             'name': 'Borra Caves',
#             'category': 'natural',
#             'description': 'Stunning limestone caves with stalactites and stalagmites, located in the Ananthagiri Hills.',
#             'location': 'Visakhapatnam',
#             'latitude': 18.2667,
#             'longitude': 82.9833,
#             'entry_fee': 50.00,
#             'visiting_hours': '10 AM - 5 PM',
#             'safety_tip': 'Follow guide instructions inside the caves.',
#             'average_rating': 4.6,
#             'visit_count': 75
#         },
#         {
#             'name': 'Manginapudi Beach',
#             'category': 'natural',
#             'description': 'A serene black sand beach near Machilipatnam, perfect for a quiet getaway.',
#             'location': 'Machilipatnam',
#             'latitude': 16.1667,
#             'longitude': 81.1333,
#             'entry_fee': 0.00,
#             'visiting_hours': 'Open 24 hours',
#             'safety_tip': 'Avoid isolated areas after sunset.',
#             'average_rating': 4.3,
#             'visit_count': 55
#         },
#         {
#             'name': 'Kurnool Fort',
#             'category': 'historical',
#             'description': 'A historic fort with remnants of the Qutb Shahi and Vijayanagara periods.',
#             'location': 'Kurnool',
#             'latitude': 15.8281,
#             'longitude': 78.0353,
#             'entry_fee': 5.00,
#             'visiting_hours': '9 AM - 5 PM',
#             'safety_tip': 'Watch for uneven terrain while exploring.',
#             'average_rating': 4.2,
#             'visit_count': 50
#         },
#         {
#             'name': 'Papikondalu',
#             'category': 'natural',
#             'description': 'A scenic range of hills along the Godavari River, ideal for boating and nature walks.',
#             'location': 'East Godavari',
#             'latitude': 17.3167,
#             'longitude': 81.7500,
#             'entry_fee': 0.00,
#             'visiting_hours': '6 AM - 6 PM',
#             'safety_tip': 'Wear life jackets during boat rides.',
#             'average_rating': 4.5,
#             'visit_count': 65
#         },
#         {
#             'name': 'Sri Venkateswara Wildlife Sanctuary',
#             'category': 'Wildlife',
#             'description': 'A biodiversity-rich sanctuary near Tirumala, home to tigers, leopards, and diverse flora.',
#             'location': 'Chittoor',
#             'latitude': 13.6667,
#             'longitude': 79.3333,
#             'entry_fee': 100.00,
#             'visiting_hours': '6 AM - 6 PM',
#             'safety_tip': 'Follow safari guidelines and avoid feeding animals.',
#             'average_rating': 4.4,
#             'visit_count': 60
#         }
#     ]

#     for place_data in places:
#         # Check if place already exists to avoid duplicates
#         if not Place.objects.filter(state=andhra_pradesh, name=place_data['name']).exists():
#             Place.objects.create(
#                 state=andhra_pradesh,
#                 name=place_data['name'],
#                 category=place_data['category'],
#                 description=place_data['description'],
#                 location=place_data['location'],
#                 latitude=place_data['latitude'],
#                 longitude=place_data['longitude'],
#                 entry_fee=place_data['entry_fee'],
#                 visiting_hours=place_data['visiting_hours'],
#                 safety_tip=place_data['safety_tip'],
#                 average_rating=place_data['average_rating'],
#                 visit_count=place_data['visit_count']
#             )
#             print(f"Inserted: {place_data['name']}")
#         else:
#             print(f"Skipped: {place_data['name']} already exists")

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
    # Fetch Kerala state (do not delete existing data)
    try:
        kerala = State.objects.get(name="Kerala")
    except State.DoesNotExist:
        print("Error: Kerala state not found. Please ensure it exists in the State model.")
        return

    # Insert new places for Kerala
    places = [
        {
            'name': 'Sabarimala Temple',
            'category': 'religious',
            'description': 'A major Hindu pilgrimage site dedicated to Lord Ayyappa, located in the Periyar Tiger Reserve.',
            'location': 'Sabarimala',
            'latitude': 9.4340,
            'longitude': 77.0870,
            'entry_fee': 0.00,
            'visiting_hours': 'Pilgrimage season: November to mid-January, 4 AM - 1 PM, 3 PM - 11 PM',
            'safety_tip': 'Follow strict dress codes (black/saffron) and obtain virtual queue tickets.',
            'average_rating': 4.8,
            'visit_count': 90
        },
        {
            'name': 'Varkala Beach',
            'category': 'natural',
            'description': 'A unique cliff beach with mineral springs and a serene ambiance, ideal for relaxation.',
            'location': 'Varkala',
            'latitude': 8.7333,
            'longitude': 76.7167,
            'entry_fee': 0.00,
            'visiting_hours': 'Open 24 hours',
            'safety_tip': 'Avoid swimming in unpatrolled areas due to strong currents.',
            'average_rating': 4.6,
            'visit_count': 85
        },
        {
            'name': 'Bekal Fort',
            'category': 'historical',
            'description': 'A 17th-century fort overlooking the Arabian Sea, known for its scenic beauty and architecture.',
            'location': 'Bekal',
            'latitude': 12.3911,
            'longitude': 75.0300,
            'entry_fee': 20.00,
            'visiting_hours': '8 AM - 5:30 PM',
            'safety_tip': 'Watch for slippery surfaces near the fort walls.',
            'average_rating': 4.7,
            'visit_count': 75
        },
        {
            'name': 'Wayanad Wildlife Sanctuary',
            'category': 'Wildlife',
            'description': 'A biodiversity hotspot with elephants, tigers, and scenic trails in the Western Ghats.',
            'location': 'Wayanad',
            'latitude': 11.6500,
            'longitude': 76.0833,
            'entry_fee': 150.00,
            'visiting_hours': '7 AM - 5 PM',
            'safety_tip': 'Follow guide instructions during safaris and avoid stray paths.',
            'average_rating': 4.5,
            'visit_count': 70
        },
        {
            'name': 'Padmanabhaswamy Temple',
            'category': 'religious',
            'description': 'A historic temple dedicated to Lord Vishnu, famous for its architectural grandeur and treasures.',
            'location': 'Thiruvananthapuram',
            'latitude': 8.9496,
            'longitude': 76.5712,
            'entry_fee': 0.00,
            'visiting_hours': '3:30 AM - 11 AM, 5 PM - 7:30 PM',
            'safety_tip': 'Strict dress code (dhoti for men, saree for women) and no photography allowed.',
            'average_rating': 4.8,
            'visit_count': 95
        },
        {
            'name': 'Athirappilly Falls',
            'category': 'natural',
            'description': 'A majestic waterfall in the Western Ghats, often called the "Niagara of India."',
            'location': 'Thrissur',
            'latitude': 10.2876,
            'longitude': 76.5667,
            'entry_fee': 20.00,
            'visiting_hours': '8 AM - 5 PM',
            'safety_tip': 'Stay behind barriers to avoid slipping near the falls.',
            'average_rating': 4.7,
            'visit_count': 80
        },
        {
            'name': 'Mattancherry Palace',
            'category': 'historical',
            'description': 'A 16th-century Portuguese palace with stunning murals, reflecting Kerala’s colonial history.',
            'location': 'Kochi',
            'latitude': 9.9620,
            'longitude': 76.2610,
            'entry_fee': 5.00,
            'visiting_hours': '9 AM - 5 PM',
            'safety_tip': 'Remove shoes before entering the palace interiors.',
            'average_rating': 4.6,
            'visit_count': 70
        },
        {
            'name': 'Periyar National Park',
            'category': 'Wildlife',
            'description': 'A tiger reserve with boat safaris on Periyar Lake, home to elephants and diverse wildlife.',
            'location': 'Thekkady',
            'latitude': 9.5667,
            'longitude': 77.1833,
            'entry_fee': 200.00,
            'visiting_hours': '6 AM - 6 PM',
            'safety_tip': 'Wear neutral colors and avoid feeding animals during safaris.',
            'average_rating': 4.6,
            'visit_count': 75
        },
        {
            'name': 'Thrissur Pooram',
            'category': 'cultural',
            'description': 'A grand annual temple festival with elephant processions, fireworks, and traditional music.',
            'location': 'Thrissur',
            'latitude': 10.5270,
            'longitude': 76.2144,
            'entry_fee': 0.00,
            'visiting_hours': 'Festival-specific, typically April/May',
            'safety_tip': 'Maintain distance from elephants and avoid crowded areas.',
            'average_rating': 4.7,
            'visit_count': 85
        },
        {
            'name': 'Kumarakom Bird Sanctuary',
            'category': 'Wildlife',
            'description': 'A haven for migratory birds along the Vembanad Lake, perfect for birdwatching.',
            'location': 'Kumarakom',
            'latitude': 9.6167,
            'longitude': 76.4333,
            'entry_fee': 50.00,
            'visiting_hours': '6:30 AM - 6 PM',
            'safety_tip': 'Carry binoculars and avoid disturbing nesting birds.',
            'average_rating': 4.5,
            'visit_count': 65
        },
        {
            'name': 'Cherai Beach',
            'category': 'natural',
            'description': 'A peaceful beach near Kochi with golden sands and shallow waters, ideal for families.',
            'location': 'Kochi',
            'latitude': 10.1720,
            'longitude': 76.1850,
            'entry_fee': 0.00,
            'visiting_hours': 'Open 24 hours',
            'safety_tip': 'Check tide schedules before swimming.',
            'average_rating': 4.4,
            'visit_count': 70
        },
        {
            'name': 'Malampuzha Dam',
            'category': 'natural',
            'description': 'A scenic dam with gardens, a ropeway, and boating facilities in the Palakkad region.',
            'location': 'Palakkad',
            'latitude': 10.8500,
            'longitude': 76.6833,
            'entry_fee': 10.00,
            'visiting_hours': '9 AM - 5 PM',
            'safety_tip': 'Use life jackets during boating and avoid cliff edges.',
            'average_rating': 4.5,
            'visit_count': 60
        },
        {
            'name': 'Parambikulam Wildlife Sanctuary',
            'category': 'Wildlife',
            'description': 'A tiger reserve with dense forests, teak plantations, and boat safaris on the Parambikulam Lake.',
            'location': 'Palakkad',
            'latitude': 10.4000,
            'longitude': 76.7833,
            'entry_fee': 150.00,
            'visiting_hours': '7 AM - 6 PM',
            'safety_tip': 'Book safaris in advance and follow park rules.',
            'average_rating': 4.6,
            'visit_count': 65
        },
        {
            'name': 'Kovalam Beach',
            'category': 'natural',
            'description': 'A famous beach with crescent-shaped shores, lighthouse views, and Ayurvedic resorts.',
            'location': 'Thiruvananthapuram',
            'latitude': 8.3900,
            'longitude': 76.9783,
            'entry_fee': 0.00,
            'visiting_hours': 'Open 24 hours',
            'safety_tip': 'Swim only in lifeguard-monitored areas.',
            'average_rating': 4.6,
            'visit_count': 80
        },
        {
            'name': 'Hill Palace Museum',
            'category': 'cultural',
            'description': 'A former royal palace turned museum, showcasing Kerala’s royal heritage and artifacts.',
            'location': 'Tripunithura',
            'latitude': 9.9440,
            'longitude': 76.3410,
            'entry_fee': 10.00,
            'visiting_hours': '10 AM - 5:30 PM',
            'safety_tip': 'No photography inside the museum; respect displayed items.',
            'average_rating': 4.5,
            'visit_count': 70
        }
    ]

    for place_data in places:
        # Check if place already exists to avoid duplicates
        if not Place.objects.filter(state=kerala, name=place_data['name']).exists():
            Place.objects.create(
                state=kerala,
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