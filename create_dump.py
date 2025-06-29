#!/usr/bin/env python
"""
Script to update place images and create a JSON dump for Render deployment.
Run this script from the project root directory.
"""

import os
import sys
import django
import subprocess

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'south_india_tourism.settings')
django.setup()

from core.models import Place
from django.db import transaction

def update_place_images():
    """Update image URLs for places"""
    
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
        'Kochi': 'https://th.bing.com/th/id/OIP.swbfNvs1t4jiBw0shTIkDAHaFj?w=251&h=188&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
        'Alleppey': 'https://th.bing.com/th/id/OIP.swbfNvs1t4jiBw0shTIkDAHaFj?w=251&h=188&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
        'Munnar': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Munnar_Top_station.jpg/500px-Munnar_Top_station.jpg',
        
        # Andhra Pradesh places
        'Sri Venkateswara Wildlife Sanctuary': 'https://th.bing.com/th/id/OIP.NYRxSHw6TQKA6WFmIXHUBgHaE7?w=242&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
        'Papikondalu': 'https://th.bing.com/th/id/OIP.K7SfTNId5QMW9IKzwIRM7AHaEH?w=362&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
        'Kurnool Fort': 'https://tse2.mm.bing.net/th/id/OIP.PR8TCgugKhfDZIM5ssJ--QHaEh?pid=ImgDet&w=185&h=112&c=7&dpr=1.3&o=7&rm=3',
        'Bhadrachalam Temple': 'https://th.bing.com/th/id/OIP.e7HNodOrqbTyrbxSqmZ-lgHaFY?w=259&h=187&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
        'Vijayawada': 'https://www.bing.com/th/id/OIP.JNnpFTXLwr9xPpQiD1wG4AHaE8?w=173&h=185&c=8&rs=1&qlt=90&o=6&dpr=1.3&pid=3.1&rm=2',
        'Araku Valley': 'https://ts2.mm.bing.net/th?id=OIP.Z2Q9tHq43TT_a0MUmS3HbAHaFj&pid=15.1',
        'Tirupati': 'https://th.bing.com/th/id/OIP.3KbZNVRPZYNDovYN8-OUdAHaE7?w=255&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
        
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
        'Kanyakumari Beach': 'https://th.bing.com/th?id=OLC.B4j%2fMmSBHuCF0w480x360&w=249&h=140&c=8&rs=1&qlt=90&o=6&dpr=1.3&pid=3.1&rm=2',
        'Sterling Ooty - Fern Hill': 'https://th.bing.com/th/id/OIP.pUHUaxntQOo1w304YYspHwHaF7?w=162&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
        'Govt. Museum Madurai': 'https://th.bing.com/th/id/OIP.vO_6BmTtk5dlPA0AxCVtPgHaE2?w=211&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
        'Doddabetta Ooty Highest Point': 'https://th.bing.com/th/id/OLC.6jA9MfEvyrFVBQ480x360?w=209&h=140&c=8&rs=1&qlt=90&o=6&dpr=1.3&pid=3.1&rm=2',
        'Government Botanical Garden': 'https://th.bing.com/th/id/OIP.7jLFJ4SMOdn37yQdAn6T0wHaE5?w=230&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
        'Government Museum': 'https://cdn.getyourguide.com/img/tour/4bc83b4edc13379afb6013be57bdea9777ccaa36420634b4c085ddc930f8784f.jpg/132.webp',
        'Mahabalipuram': 'https://th.bing.com/th/id/OSK.HEROMtRcivR4UZG9df5pGHUZEngp3Zn6G8SP_XrGzecs_Wg?w=312&h=200&c=7&rs=1&o=6&dpr=1.3&pid=SANGAM',
        'Ooty Hill Station': 'https://th.bing.com/th/id/OIP.nQRjc0uzpiCmp3HQ2Pt_DQHaGa?w=195&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
        'Meenakshi Temple': 'https://th.bing.com/th/id/OIP.LMhlulnHB23RjxBNU-m4OwHaFQ?w=217&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
        'Marina Beach': 'https://th.bing.com/th/id/OIP.q6kDQLnsaRxi5XPGIrg_-wHaD-?w=261&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
        
        # Telangana places
        'Nizamabad': 'https://th.bing.com/th/id/OSK.HEROhb3olG-r2SARJhN1bUpLJop0uYj7gkRS1Bwnma3Lf1I?w=312&h=200&c=15&rs=2&o=6&dpr=1.3&pid=SANGAM',
        'Warangal': 'https://th.bing.com/th/id/OIP.ozI4X2GkmXhM793MnYMIUQHaGL?w=218&h=182&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
        
        # Karnataka places
        'Mysore': 'https://th.bing.com/th/id/OIP.iIZ0RutrWVdNtXSXHB2wQAHaE8?w=204&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
        'Coorg': 'https://mycookingcanvas.com/wp-content/uploads/2017/10/DSC_0873.jpg',
        'Hampi': 'https://th.bing.com/th/id/OIP.RyeAjBtEEQwzUnpAbXGSRgHaE9?w=263&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
    }

    updated_count = 0
    not_found_count = 0
    not_found_places = []

    print("🔄 Updating place images...")
    print("=" * 60)

    with transaction.atomic():
        for place_name, image_url in place_images.items():
            try:
                # Try to find the place by name (case-insensitive)
                place = Place.objects.filter(name__icontains=place_name).first()
                
                if place:
                    place.image_url = image_url
                    place.save()
                    updated_count += 1
                    print(f"✅ Updated: {place.name} ({place.state.name})")
                else:
                    not_found_count += 1
                    not_found_places.append(place_name)
                    print(f"⚠️  Not found: {place_name}")
                    
            except Exception as e:
                print(f"❌ Error updating {place_name}: {str(e)}")

    print(f"\n✅ Successfully updated {updated_count} places")
    
    if not_found_count > 0:
        print(f"⚠️  {not_found_count} places not found:")
        for place in not_found_places:
            print(f"   - {place}")

def create_dump():
    """Create JSON dump using Django's dumpdata command"""
    print("\n🔄 Creating JSON dump...")
    print("=" * 60)
    
    try:
        # Create the dump using Django's dumpdata command
        result = subprocess.run([
            'python', 'manage.py', 'dumpdata', 'core'
        ], capture_output=True, text=True, check=True)
        
        # Write the output to core_data.json
        with open('core_data.json', 'w') as f:
            f.write(result.stdout)
        
        print("✅ Successfully created core_data.json")
        print(f"📄 File size: {len(result.stdout)} characters")
        
        # Show a preview of the file
        print("\n📋 Preview of core_data.json:")
        print("-" * 40)
        lines = result.stdout.split('\n')
        for i, line in enumerate(lines[:10]):
            print(line)
        if len(lines) > 10:
            print("...")
            print(f"... and {len(lines) - 10} more lines")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating dump: {e}")
        print(f"Error output: {e.stderr}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    # Step 1: Update place images
    update_place_images()
    
    # Step 2: Create JSON dump
    create_dump()
    
    print("\n🎉 Process completed!")
    print("📁 Files created:")
    print("   - core_data.json (ready for Render deployment)")
    print("\n🚀 To deploy to Render, use:")
    print("   DATABASE_URL=\"your_render_db_url\" python manage.py loaddata core_data.json") 