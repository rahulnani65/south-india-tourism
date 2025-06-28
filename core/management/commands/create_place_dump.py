from django.core.management.base import BaseCommand
from django.core import serializers
from core.models import Place, State
import json

class Command(BaseCommand):
    help = 'Create a JSON dump file with places and their image URLs for Render deployment'

    def handle(self, *args, **options):
        # Dictionary of place names and their image URLs
        place_images = {
            # Kerala places
            'Pathiramanal Island': 'https://th.bing.com/th/id/OIP.fu9MEoFwamUnm4Ehw3dl9QHaEK?w=283&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
            'Edava Beach': 'https://th.bing.com/th/id/OIP.aolmPJtlhgnrABEBtEQfEgHaEL?w=290&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
            'Hill Palace Museum': 'https://th.bing.com/th/id/OLC.9owyWZX18mxxsw480x360?w=212&h=140&c=8&rs=1&qlt=90&o=6&dpr=1.3&pid=3.1&rm=2',
            'Kovalam Beach': 'https://www.keralam.me/wp-content/uploads/2019/03/crescent_shaped_kovalam_beach-1024x683.jpg',
            'Parambikulam Wildlife Sanctuary': 'https://th.bing.com/th/id/OIP.nb6_wqrlbZ6R_QMYIvDjoQHaDU?w=348&h=156&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
            'Malampuzha Dam': 'https://www.keralatourism.org/images/destination/large/malampuzha_dam_and_garden20131030155415_124_1.jpg',
            'Cherai Beach': 'https://th.bing.com/th/id/OIP.8iKOyLSQMtgzhnOxNyPZ0QHaE7?w=260&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
            'Kumarakom Bird Sanctuary': 'https://th.bing.com/th/id/OIP.Tbsp9mfH31g13l6HvIYnvQHaDt?w=286&h=175&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
            'Thrissur Pooram': 'https://ts1.mm.bing.net/th?id=OIP.wqsObrnme4V2A9-MauTzygHaFj&pid=15.1',
            'Periyar National Park': 'https://th.bing.com/th/id/OIP.jbbU7Zg-_bNnIMCtpuH0mwHaEc?w=312&h=187&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
            'Athirappilly Falls': 'https://th.bing.com/th/id/OLC.x2TQiL6APxJ0dg480x360?w=244&h=140&c=8&rs=1&qlt=90&o=6&dpr=1.3&pid=3.1&rm=2',
            'Padmanabhaswamy Temple': 'https://th.bing.com/th/id/OSK.nkl8p0vP2OdOAA4NO6q-wWQCShLeQrytfGm5DVjOM5w?w=200&h=200&c=7&rs=1&o=6&dpr=1.3&pid=SANGAM',
            'Wayanad Wildlife Sanctuary': 'https://ts4.mm.bing.net/th?id=OIP.lV31NKtkd3GDBKe2QWpMJgHaDt&pid=15.1',
            'Bekal Fort': 'https://tse3.mm.bing.net/th/id/OIP.jMxg24gKYY7WLY3ytwP0sgHaE8?rs=1&pid=ImgDetMain&o=7&rm=3',
            'Varkala Beach': 'https://th.bing.com/th?id=OLC.HMsYdQcYI%2fLtUg480x360&w=276&h=140&c=8&rs=1&qlt=90&o=6&dpr=1.3&pid=3.1&rm=2',
            'Sabarimala Temple': 'https://th.bing.com/th/id/OIP.udlUUrE63U193T5PUscKrAHaEn?w=295&h=184&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
            
            # Andhra Pradesh places
            'Sri Venkateswara Wildlife Sanctuary': 'https://th.bing.com/th/id/OIP.NYRxSHw6TQKA6WFmIXHUBgHaE7?w=242&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
            'Papikondalu': 'https://th.bing.com/th/id/OIP.K7SfTNId5QMW9IKzwIRM7AHaEH?w=362&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
            'Kurnool Fort': 'https://tse2.mm.bing.net/th/id/OIP.PR8TCgugKhfDZIM5ssJ--QHaEh?pid=ImgDet&w=185&h=112&c=7&dpr=1.3&o=7&rm=3',
            'Bhadrachalam Temple': 'https://th.bing.com/th/id/OIP.e7HNodOrqbTyrbxSqmZ-lgHaFY?w=259&h=187&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
            
            # Tamil Nadu places
            'Pamban Bridge': 'https://th.bing.com/th/id/OIP.WYnIBshJrd_AYENu60wKTgHaEo?w=275&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
            'Chettinad Mansions': 'https://th.bing.com/th/id/OIP.EOxWnWZaMnB1G7BBKSjHEAHaE8?w=275&h=183&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
            'Mudumalai National Park': 'https://th.bing.com/th/id/OIP.XT1vJsnDofcSOaPDBvp9RQHaDv?w=316&h=177&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
            'Dhanushkodi Beach': 'https://www.bing.com/th/id/OIP.C0DDyjs9UIY7i14-wJYE4gHaER?w=180&h=185&c=8&rs=1&qlt=90&o=6&dpr=1.3&pid=3.1&rm=2',
            'Yercaud': 'https://th.bing.com/th/id/OIP.81CMrHorvNgCcFEoYulUrAHaE7?w=230&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
            'Kodaikanal': 'https://th.bing.com/th/id/OSK.HEROHAKGiSimWRo9YODWmWMljwNyhlhKzYxa2BY9n0XIwRY?w=312&h=200&c=15&rs=2&o=6&dpr=1.3&pid=SANGAM',
            'Gingee Fort': 'https://th.bing.com/th/id/OLC.inxFby2XaOtYRQ480x360?w=186&h=140&c=8&rs=1&qlt=90&o=6&dpr=1.3&pid=3.1&rm=2',
            'Airavateswara Temple': 'https://tse1.mm.bing.net/th/id/OIP.SG0jFhiFT5gpIJpJ8SMWXQHaE8?rs=1&pid=ImgDetMain&o=7&rm=3',
            'Kapaleeshwarar Temple': 'https://th.bing.com/th/id/OIP.Dm_lz2tIJzNQ-8uIEU7TIwHaDt?w=332&h=175&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
            'Ramanathaswamy Temple': 'https://th.bing.com/th/id/OIP.Ggnz8raWQXx4oeuK3MpGmwHaFH?w=241&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
            'Brihadeeswarar Temple': 'https://th.bing.com/th/id/OSK.HEROhjCW50bQYy7t454d2fA3aN4LdDqsCqTJKqkC3VbYoH0?w=312&h=200&c=15&rs=2&o=6&dpr=1.3&pid=SANGAM',
        }

        # First, update all places with image URLs
        updated_count = 0
        for place_name, image_url in place_images.items():
            place = Place.objects.filter(name__icontains=place_name).first()
            if place:
                place.image_url = image_url
                place.save()
                updated_count += 1
                self.stdout.write(f'Updated {place.name} with image URL')

        self.stdout.write(f'Updated {updated_count} places with image URLs')

        # Now create the JSON dump
        places = Place.objects.all()
        
        # Serialize places to JSON
        places_data = serializers.serialize('json', places, indent=2)
        
        # Write to file
        with open('core_data.json', 'w') as f:
            f.write(places_data)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created core_data.json with {places.count()} places')
        )
        
        # Also create a states dump
        states = State.objects.all()
        states_data = serializers.serialize('json', states, indent=2)
        
        with open('states_data.json', 'w') as f:
            f.write(states_data)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created states_data.json with {states.count()} states')
        ) 