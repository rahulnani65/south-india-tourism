#!/usr/bin/env python
"""
Simple script to update place images and create JSON dump.
Run: python update_and_dump.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'south_india_tourism.settings')
django.setup()

from core.models import Place
from django.db import transaction

def update_images():
    """Update place images in database"""
    
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
        'Manginapudi Beach': 'https://i.pinimg.com/736x/ed/08/fc/ed08fc966b7dbfe2eb1632e540abd5de.jpg',
        'Borra Caves': 'https://media.istockphoto.com/id/801563986/photo/borra-cave-araku-andhra-pradesh-india-travel-destination-in-india.jpg?s=612x612&w=0&k=20&c=zo2IJfRp-h4zYh1q8tKuSh_9DeJq-BY6bRscbIAHngo=',
        'Kondapalli Fort': 'https://s7ap1.scene7.com/is/image/incredibleindia/kondapalli-fort-guntur-andhra-pradesh-2-attr-hero?qlt=82&ts=1726743696048',
        'Konaseema': 'https://i.pinimg.com/736x/59/1b/d1/591bd16f56746c8e2ada6ecd6c174209.jpg',
        'Guntur Fort': 'https://media.istockphoto.com/id/1488619041/photo/kondaveedu-fort.jpg?s=612x612&w=0&k=20&c=IfJr9T8rNintCsssTPWqQCHkIhUNFUUcwtdcZfPwxEo=',
        'Kailasagiri Hill': 'https://i.pinimg.com/736x/b7/6a/a4/b76aa4230c18e9b5e3ace8264c78cd64.jpg',
        'Ahobilam Temple': 'https://i.pinimg.com/736x/58/86/1f/58861f13a28d27a311f637f954fb8b21.jpg',
        'Lambasingi': 'https://i.pinimg.com/736x/67/5b/38/675b381e0675a56052f1d04f1a94546e.jpg',
        'Amaravati Stupa': 'https://i.pinimg.com/736x/d7/e7/af/d7e7af61b15bd5b170bb5122ab459fc9.jpg',
        'Visakhapatnam Beach': 'https://i.pinimg.com/736x/c2/39/9c/c2399c7c5d5f581fe7d974936c8b9b85.jpg',
        'Srisailam Temple': 'https://i.pinimg.com/736x/45/ee/83/45ee83cc1cdce419e5e8ad3f34451484.jpg',
        
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
        'Laknavaram Lake': 'https://i.pinimg.com/736x/1b/c0/bc/1bc0bcab779d6b36fd692683c281aa4b.jpg',
        'Ramappa Temple': 'https://i.pinimg.com/736x/f5/a7/a2/f5a7a26d3dadc7dd689365f83593dfbf.jpg',
        'Sammakka Saralamma Jatara': 'https://warangaltourism.in/images/places-to-visit-warangal/headers/sammakka-saralamma-temple-warangal-tourism-entry-fee-timings-holidays-reviews-header.jpg',
        'Ananthagiri Hills': 'https://i.pinimg.com/736x/c5/30/23/c53023724e7e256e35ea29228d2dc52b.jpg',
        'Medak Cathedral': 'https://i.pinimg.com/736x/f2/6c/76/f26c76ecdde69b19d480f0fb386b5a85.jpg',
        'Pocharam Wildlife Sanctuary': 'https://i.pinimg.com/736x/2b/5a/5e/2b5a5eed48e0608855551cfdf6fa69c2.jpg',
        'Kawal Wildlife Sanctuary': 'https://uniquelytelangana.in/wp-content/uploads/2023/11/thehindu-768x531.jpg',
        'Kala Ashram': 'https://www.telanganafirst.in/wp-content/uploads/2018/04/GurujiTELAN30apr2018.jpg',
        'Ramoji Film City': 'https://i.pinimg.com/736x/81/7c/f5/817cf5c3f147306208dc9df54dec9392.jpg',
        'Pakhal Lake': 'https://dynamic-media-cdn.tripadvisor.com/media/photo-o/15/c0/b6/17/the-panaroma-ciew.jpg?w=900&h=500&s=1',
        'Kuntala Waterfall': 'https://imgstaticcontent.lbb.in/lbbnew/wp-content/uploads/2018/05/24143309/Kuntala.png',
        'Bhongir Fort': 'https://www.gosahin.com/go/p/e/1528632119_Bhongir-Fort1.jpg',
        'Thousand Pillar Temple': 'https://i.pinimg.com/736x/18/44/88/184488289abc048b014dae5300e86865.jpg',
        'Yadagirigutta Temple': 'https://i.pinimg.com/736x/c8/f9/40/c8f9405b6e5b1d522a1b43bcc0a3c648.jpg',
        
        # Karnataka places
        'Mysore': 'https://th.bing.com/th/id/OIP.iIZ0RutrWVdNtXSXHB2wQAHaE8?w=204&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
        'Coorg': 'https://mycookingcanvas.com/wp-content/uploads/2017/10/DSC_0873.jpg',
        'Hampi': 'https://th.bing.com/th/id/OIP.RyeAjBtEEQwzUnpAbXGSRgHaE9?w=263&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3',
        'Bandipur National Park': 'https://dwq3yv87q1b43.cloudfront.net/public/blogs/fit-in/1200x675/Blog_20250129-1838355028-1738150232.jpg',
        'Sakleshpur': 'https://media1.thrillophilia.com/filestore/4n4bisg1bhdalayj9iw6sotm370j_1607434010_shutterstock_1602889177.jpg?w=400&dpr=2',
        'Lalbagh Botanical Garden': 'https://media.istockphoto.com/id/1382865466/photo/bangalore-or-bengaluru.jpg?s=612x612&w=0&k=20&c=4Vm2X10GG8fmNSUnKiUepxs7spvExtrFY7lLYKGHjEs=',
        'Karwar Beach': 'https://i.pinimg.com/736x/c2/42/36/c2423675dec048f7d1a5fe655337198a.jpg',
        'Kollur Mookambika Temple': 'https://media.istockphoto.com/id/2155978659/photo/thousand-pillars-jain-temple-ancient-temple-located-in-moodbidri-and-visited-by-devotees-and.jpg?s=612x612&w=0&k=20&c=McjJEoTsouI0dZdR5EaKYZGYHy2bgqt-jZD5v5On9rE=',
        'Kabini Wildlife Sanctuary': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSN2jGOxniomMSnK4z41ROKYrqwNekL-yxnVQ&s',
        'Bijapur Gol Gumbaz': 'https://i.pinimg.com/736x/03/94/b3/0394b3df68b062b971155f99ac37aeb4.jpg',
        'Agumbe Rainforest': 'https://assets.zeezest.com/blogs/PROD_Agumbe,%20Karnataka%20Top%20Places%20to%20Visit,%20Things%20to%20Do,%20and%20Best%20Time%20for%20a%20Rainforest%20Trip%20(1)_1722003600967_thumb_1200.jpeg',
        'Dharmasthala Manjunatha Temple': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTLZ_YyfwANTksrWSICRlYoP4wILx5mMbcr0A&s',
        'Pattadakal': 'https://upload.wikimedia.org/wikipedia/commons/0/03/Pattadakal_000.JPG',
        'Kudremukh National Park': 'https://i.pinimg.com/736x/48/df/5d/48df5d7339db9fcb254872b23f82206a.jpg',
        'Murudeshwar Temple': 'https://media.istockphoto.com/id/1268998403/photo/murdeshwar-temple-early-morning-view-from-low-angle-image.jpg?s=612x612&w=0&k=20&c=2GiW8vZM8iLnTDGhffunntYfh4zhYw8SY656-124CT0=',
        'Vidhana Soudha': 'https://i.pinimg.com/736x/67/91/70/679170e29c303ce2326ae5e613074825.jpg',
        'Shravanabelagola': 'https://media.istockphoto.com/id/586356630/photo/the-statue-of-gomateswara-bahubali.jpg?s=612x612&w=0&k=20&c=39I6T9ObHxUDEq6wW9XNEEJLNJ4rM2eEsEECu-CISnI=',
        'Nandi Hills': 'https://i.pinimg.com/736x/79/19/0d/79190de81fdd68ebb265d47e5f437c44.jpg',
        'Bannerghatta National Park': 'https://www.bangaloreanx.com/wp-content/uploads/2025/03/Untitled-design-5.jpg',
        'Gokarna Beach': 'https://media.istockphoto.com/id/1181378413/photo/sunset-at-gokarna-beach-karnataka-india.jpg?s=612x612&w=0&k=20&c=kL7aR5ohESZraQzHP8ZUzNW9SarefWYVigf_vrCai0I=',
        'Udupi Sri Krishna Temple': 'https://i.pinimg.com/736x/63/14/27/6314278b2bde772977e7ef0f07656399.jpg',
        'Dandeli Wildlife Sanctuary': 'https://i0.wp.com/kaziranganationalparkassam.in/wp-content/uploads/2021/07/IMG-20210711-WA0007.jpg?ssl=1',
        'Chikmagalur': 'https://shanthikunnj.com/assets/img/news/discover-mullayanagiri-peak-chikmagalurs-highest-point.jpg',
        'Belur Halebidu Temples': 'https://www.karnatakatravel.com/wp-content/uploads/2019/11/belur_halebidu.jpg',
        'Jog Falls': 'https://i.pinimg.com/736x/e8/98/ea/e898ead86d41657c56e9a8bfce3938f0.jpg',
        'Sringeri Sharada Peetham': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Vidyashankara_Temple_at_Shringeri.jpg/1200px-Vidyashankara_Temple_at_Shringeri.jpg',
        'Badami Cave Temples': 'https://media.istockphoto.com/id/1742429799/photo/entrance-to-the-ancient-rock-cut-caves-of-badami-karnataka-india.jpg?s=612x612&w=0&k=20&c=Vi9quFLEXAD8EfBM8ICOBWxyI2lwM4EyH0jq4JZqeIQ=',
    }

    updated = 0
    not_found = []
    skipped = 0

    with transaction.atomic():
        for place_name, image_url in place_images.items():
            place = Place.objects.filter(name__icontains=place_name).first()
            if place:
                # Check if place already has an image URL
                if place.image_url:
                    print(f"⏭️  Skipped (already has image): {place.name}")
                    skipped += 1
                    continue
                
                # Truncate URL if it's too long (max 200 chars for safety)
                if len(image_url) > 200:
                    # Try to find a shorter version or truncate
                    if '?' in image_url:
                        # Remove query parameters
                        base_url = image_url.split('?')[0]
                        if len(base_url) <= 200:
                            image_url = base_url
                        else:
                            # Truncate to 200 chars
                            image_url = image_url[:200]
                    else:
                        # Truncate to 200 chars
                        image_url = image_url[:200]
                
                try:
                    place.image_url = image_url
                    place.save()
                    updated += 1
                    print(f"✅ {place.name}")
                except Exception as e:
                    print(f"❌ Error updating {place.name}: {str(e)}")
            else:
                not_found.append(place_name)

    print(f"\n✅ Updated {updated} places")
    print(f"⏭️  Skipped {skipped} places (already had images)")
    if not_found:
        print(f"⚠️ Not found: {', '.join(not_found)}")

def create_json():
    """Create JSON dump using Django's dumpdata"""
    import subprocess
    
    print("\n🔄 Creating JSON dump...")
    result = subprocess.run(['python', 'manage.py', 'dumpdata', 'core'], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        # Create JSON with a different name
        filename = 'south_india_tourism_data.json'
        with open(filename, 'w') as f:
            f.write(result.stdout)
        print(f"✅ Created {filename}")
        print(f"📄 File size: {len(result.stdout)} characters")
    else:
        print(f"❌ Error: {result.stderr}")

if __name__ == "__main__":
    print("🔄 Updating place images...")
    update_images()
    create_json()
    print("\n🎉 Done! Run: python manage.py loaddata south_india_tourism_data.json") 