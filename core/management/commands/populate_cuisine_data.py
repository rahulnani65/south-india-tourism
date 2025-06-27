from django.core.management.base import BaseCommand
from core.models import State, Cuisine, Restaurant

class Command(BaseCommand):
    help = 'Populate cuisine and restaurant data for South Indian states'

    def handle(self, *args, **options):
        self.stdout.write('Populating cuisine and restaurant data...')
        
        # Kerala Cuisine Data
        kerala = State.objects.get(name='Kerala')
        
        kerala_cuisines = [
            {
                'name': 'Kerala Sadya',
                'description': 'A traditional vegetarian feast served on banana leaves with over 20 dishes including rice, sambar, rasam, avial, thoran, and payasam. This elaborate meal is served during festivals and special occasions.'
            },
            {
                'name': 'Kerala Fish Curry',
                'description': 'Spicy fish curry made with coconut milk, tamarind, and aromatic spices. Popular varieties include karimeen (pearl spot fish) curry and chemmeen (prawn) curry.'
            },
            {
                'name': 'Appam with Stew',
                'description': 'Soft, fluffy rice pancakes served with vegetable or chicken stew. The appam has a crispy edge and soft center, perfect for soaking up the flavorful stew.'
            },
            {
                'name': 'Puttu and Kadala Curry',
                'description': 'Steamed rice cake cylinders served with black chickpea curry. A popular breakfast dish that is both nutritious and delicious.'
            },
            {
                'name': 'Malabar Biryani',
                'description': 'Aromatic rice dish cooked with meat, spices, and herbs. The Malabar version is known for its unique blend of spices and the use of short-grain rice.'
            }
        ]
        
        kerala_restaurants = [
            {
                'name': 'Grand Hotel',
                'specialty': 'Traditional Kerala Sadya',
                'average_cost': 800.00
            },
            {
                'name': 'Paragon Restaurant',
                'specialty': 'Malabar Biryani',
                'average_cost': 600.00
            },
            {
                'name': 'Kashi Art Cafe',
                'specialty': 'Fusion Kerala Cuisine',
                'average_cost': 1200.00
            },
            {
                'name': 'Kayees Rahmathulla',
                'specialty': 'Kerala Fish Curry',
                'average_cost': 500.00
            },
            {
                'name': 'Ariya Nivaas',
                'specialty': 'Appam and Stew',
                'average_cost': 400.00
            }
        ]
        
        # Karnataka Cuisine Data
        karnataka = State.objects.get(name='Karnataka')
        
        karnataka_cuisines = [
            {
                'name': 'Bisi Bele Bath',
                'description': 'A spicy rice dish made with lentils, vegetables, and aromatic spices. This one-pot meal is a signature dish of Karnataka and is often served with papad and raita.'
            },
            {
                'name': 'Mangalorean Fish Curry',
                'description': 'Spicy fish curry from the coastal region of Mangalore, made with coconut, tamarind, and red chilies. Known for its fiery taste and rich flavors.'
            },
            {
                'name': 'Ragi Mudde',
                'description': 'Steamed finger millet balls served with spicy curry. A traditional rural dish that is highly nutritious and filling.'
            },
            {
                'name': 'Mysore Masala Dosa',
                'description': 'Crispy dosa served with potato filling and coconut chutney. The Mysore version is known for its red chutney spread inside the dosa.'
            },
            {
                'name': 'Coorg Pandi Curry',
                'description': 'Spicy pork curry from the Coorg region, made with local spices and vinegar. A must-try for meat lovers visiting Karnataka.'
            }
        ]
        
        karnataka_restaurants = [
            {
                'name': 'MTR (Mavalli Tiffin Room)',
                'specialty': 'Traditional Karnataka Breakfast',
                'average_cost': 300.00
            },
            {
                'name': 'Koshy\'s',
                'specialty': 'Mangalorean Fish Curry',
                'average_cost': 700.00
            },
            {
                'name': 'Vidyarthi Bhavan',
                'specialty': 'Mysore Masala Dosa',
                'average_cost': 150.00
            },
            {
                'name': 'Coorg Cuisine',
                'specialty': 'Coorg Pandi Curry',
                'average_cost': 800.00
            },
            {
                'name': 'The Only Place',
                'specialty': 'Bisi Bele Bath',
                'average_cost': 400.00
            }
        ]
        
        # Andhra Pradesh Cuisine Data
        andhra_pradesh = State.objects.get(name='Andhra Pradesh')
        
        andhra_cuisines = [
            {
                'name': 'Andhra Chicken Curry',
                'description': 'Spicy chicken curry made with red chilies, tamarind, and aromatic spices. Known for its fiery taste and rich gravy.'
            },
            {
                'name': 'Gongura Pachadi',
                'description': 'Tangy chutney made with sorrel leaves, red chilies, and spices. A traditional accompaniment that adds a unique sour taste to meals.'
            },
            {
                'name': 'Pesarattu',
                'description': 'Green gram dosa served with ginger chutney. A healthy breakfast option that is both nutritious and delicious.'
            },
            {
                'name': 'Andhra Biryani',
                'description': 'Fragrant rice dish cooked with meat, spices, and herbs. The Andhra version is known for its spicy taste and generous use of chilies.'
            },
            {
                'name': 'Gutti Vankaya',
                'description': 'Stuffed brinjal curry made with ground spices and tamarind. A vegetarian delicacy that showcases the region\'s love for spicy food.'
            }
        ]
        
        andhra_restaurants = [
            {
                'name': 'Rayalaseema Ruchulu',
                'specialty': 'Andhra Chicken Curry',
                'average_cost': 600.00
            },
            {
                'name': 'Spice Garden',
                'specialty': 'Andhra Biryani',
                'average_cost': 500.00
            },
            {
                'name': 'Gongura',
                'specialty': 'Traditional Andhra Thali',
                'average_cost': 400.00
            },
            {
                'name': 'Pesarattu House',
                'specialty': 'Pesarattu and Upma',
                'average_cost': 200.00
            },
            {
                'name': 'Andhra Spice',
                'specialty': 'Gutti Vankaya',
                'average_cost': 350.00
            }
        ]
        
        # Telangana Cuisine Data
        telangana = State.objects.get(name='Telangana')
        
        telangana_cuisines = [
            {
                'name': 'Hyderabadi Biryani',
                'description': 'Famous aromatic rice dish cooked with meat, saffron, and spices. The Hyderabadi version is known for its dum cooking method and rich flavors.'
            },
            {
                'name': 'Mirchi ka Salan',
                'description': 'Spicy curry made with green chilies, peanuts, and sesame seeds. A traditional accompaniment to biryani that adds heat and flavor.'
            },
            {
                'name': 'Double ka Meetha',
                'description': 'Sweet bread pudding made with fried bread, milk, and nuts. A traditional dessert served during festivals and special occasions.'
            },
            {
                'name': 'Bagara Baingan',
                'description': 'Spicy brinjal curry made with ground spices and tamarind. A vegetarian dish that is rich in flavors and textures.'
            },
            {
                'name': 'Qubani ka Meetha',
                'description': 'Sweet dish made with dried apricots, nuts, and cream. A royal dessert that showcases the region\'s Persian influences.'
            }
        ]
        
        telangana_restaurants = [
            {
                'name': 'Paradise Biryani',
                'specialty': 'Hyderabadi Biryani',
                'average_cost': 400.00
            },
            {
                'name': 'Bawarchi',
                'specialty': 'Traditional Hyderabadi Cuisine',
                'average_cost': 600.00
            },
            {
                'name': 'Cafe Bahar',
                'specialty': 'Mirchi ka Salan',
                'average_cost': 500.00
            },
            {
                'name': 'Shadab',
                'specialty': 'Bagara Baingan',
                'average_cost': 450.00
            },
            {
                'name': 'Hotel Shadab',
                'specialty': 'Double ka Meetha',
                'average_cost': 200.00
            }
        ]
        
        # Tamil Nadu Cuisine Data
        tamil_nadu = State.objects.get(name='Tamil Nadu')
        
        tamil_nadu_cuisines = [
            {
                'name': 'Idli Sambar',
                'description': 'Steamed rice cakes served with lentil soup and coconut chutney. A healthy breakfast staple that is loved across India.'
            },
            {
                'name': 'Chettinad Chicken',
                'description': 'Spicy chicken curry from the Chettinad region, made with a unique blend of spices and aromatics. Known for its bold flavors and rich taste.'
            },
            {
                'name': 'Pongal',
                'description': 'Rice and lentil dish cooked with ghee and black pepper. A traditional breakfast dish that is both nutritious and comforting.'
            },
            {
                'name': 'Rasam',
                'description': 'Spicy and tangy soup made with tamarind, tomatoes, and spices. A traditional accompaniment that aids digestion.'
            },
            {
                'name': 'Filter Coffee',
                'description': 'Strong coffee made with chicory and served with frothy milk. A cultural icon of Tamil Nadu that is enjoyed throughout the day.'
            }
        ]
        
        tamil_nadu_restaurants = [
            {
                'name': 'Murugan Idli Shop',
                'specialty': 'Idli Sambar',
                'average_cost': 100.00
            },
            {
                'name': 'Annalakshmi',
                'specialty': 'Traditional Tamil Thali',
                'average_cost': 500.00
            },
            {
                'name': 'Karaikudi',
                'specialty': 'Chettinad Chicken',
                'average_cost': 700.00
            },
            {
                'name': 'Adyar Ananda Bhavan',
                'specialty': 'Traditional Sweets',
                'average_cost': 300.00
            },
            {
                'name': 'Ratna Cafe',
                'specialty': 'Filter Coffee',
                'average_cost': 50.00
            }
        ]
        
        # Create data for each state
        states_data = {
            'Kerala': (kerala_cuisines, kerala_restaurants),
            'Karnataka': (karnataka_cuisines, karnataka_restaurants),
            'Andhra Pradesh': (andhra_cuisines, andhra_restaurants),
            'Telangana': (telangana_cuisines, telangana_restaurants),
            'Tamil Nadu': (tamil_nadu_cuisines, tamil_nadu_restaurants)
        }
        
        for state_name, (cuisines, restaurants) in states_data.items():
            state = State.objects.get(name=state_name)
            
            # Clear existing data
            Cuisine.objects.filter(state=state).delete()
            Restaurant.objects.filter(state=state).delete()
            
            # Add cuisines
            for cuisine_data in cuisines:
                Cuisine.objects.create(
                    state=state,
                    name=cuisine_data['name'],
                    description=cuisine_data['description']
                )
            
            # Add restaurants
            for restaurant_data in restaurants:
                Restaurant.objects.create(
                    state=state,
                    name=restaurant_data['name'],
                    specialty=restaurant_data['specialty'],
                    average_cost=restaurant_data['average_cost']
                )
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully populated data for {state_name}')
            )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated all cuisine and restaurant data!')
        ) 