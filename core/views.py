import requests
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count
from django.views.decorators.http import require_GET
from django.core.cache import cache
from .models import State, Contact, Hotel, Place, UserProfile, Favorite, Review, Post, Itinerary, TransportationOption, Inquiry
from .forms import UserProfileForm
from django.conf import settings
from composio_openai import ComposioToolSet, Action, App
from datetime import datetime
import pytz
import google.generativeai as genai
import logging
from django.db import transaction
import json
from django.utils.timesince import timesince
from django.utils.timezone import now
from django.views.decorators.cache import cache_page

logger = logging.getLogger(__name__)

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

@cache_page(60 * 15)
def home(request):
    states = State.objects.all()
    posts = Post.objects.all().order_by('-created_at')[:3]
    return render(request, 'core/index.html', {'states': states, 'posts': posts})

#@cache_page(60 * 15)
def state_detail(request, state_slug):
    state = get_object_or_404(State, name__iexact=state_slug.replace('-', ' '))
    places = Place.objects.filter(state=state)
    hotels = Hotel.objects.filter(place__state=state)
    reviews = Review.objects.filter(place__state=state).order_by('-created_at')[:5]
    itineraries = Itinerary.objects.filter(state=state).order_by('day')
    transport_options = TransportationOption.objects.filter(state=state)
    
    # Get the template name based on the state
    template_name = f'core/states/{state.name.lower().replace(" ", "_")}.html'
    
    # If state-specific template doesn't exist, use the default state template
    if not os.path.exists(os.path.join(settings.BASE_DIR, 'core', 'templates', template_name)):
        template_name = 'core/state.html'
    
    # Get weather data for each place
    places_with_weather = []
    for place in places:
        place_data = {
            'place': place,
            'weather': get_weather_data(place.location) if place.location else None,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'is_favorite': request.user.is_authenticated and place.favorited_by.filter(id=request.user.id).exists()
        }
        places_with_weather.append(place_data)
    
    # Check if the state is in user's favorites
    is_favorite = request.user.is_authenticated and state.favorites.filter(id=request.user.id).exists()
    
    context = {
        'state': state,
        'places_with_weather': places_with_weather,
        'hotels': hotels,
        'reviews': reviews,
        'itineraries': itineraries,
        'transport_options': transport_options,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
        'is_favorite': is_favorite
    }
    return render(request, template_name, context)

def get_weather_data(city):
    api_key = settings.OPENWEATHERMAP_API_KEY
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            weather_data = {
                'city': city,
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'condition': data['weather'][0]['description'].capitalize(),
                'icon': data['weather'][0]['icon'],
                'wind_speed': data['wind']['speed'],
            }
            suggestions = []
            safety_tips = []
            temp = weather_data['temperature']
            condition = weather_data['condition'].lower()
            
            if "rain" in condition:
                suggestions.append(f"It's raining in {city}—visit indoor attractions.")
                safety_tips.append("Carry an umbrella and avoid outdoor activities.")
            elif temp > 30:
                suggestions.append(f"It's hot today in {city}—stay hydrated and visit shaded spots.")
                safety_tips.append("Wear sunscreen and light clothing to protect against the heat.")
            else:
                suggestions.append(f"It's a pleasant day in {city}—perfect for outdoor activities!")
                safety_tips.append("Keep an eye on your belongings in crowded areas.")
            
            weather_data['suggestions'] = suggestions
            weather_data['safety_tips'] = safety_tips
            return weather_data
    except Exception as e:
        logger.error(f"Error fetching weather data: {e}")
    return None

@cache_page(60 * 15)
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    is_favorited = request.user.is_authenticated and post.favorites.filter(id=request.user.id).exists()
    return render(request, 'core/post_detail.html', {'post': post, 'is_favorited': is_favorited})

def contact_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        Contact.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )
        messages.success(request, "Your message has been sent successfully!")
        return redirect('home')
    return redirect('home')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, "Registration successful! Welcome!")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
            return render(request, 'registration/signup.html', {'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@cache_page(60 * 15)
def profile(request):
    # Ensure the user has a UserProfile, create one if it doesn't exist
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('core:profile')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'core/profile.html', {'form': form})

@login_required
def add_review(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    is_ajax = (
        request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        or request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    )
    if not place.state:
        if is_ajax:
            return JsonResponse({'success': False, 'error': 'Place has no associated state.'}, status=400)
        messages.error(request, "Cannot add review: Place has no associated state.")
        return redirect('state_detail', state_name='tamil-nadu')
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        try:
            with transaction.atomic():
                review = Review(
                    user=request.user,
                    place=place,
                    state=place.state,
                    rating=rating,
                    comment=comment
                )
                review.save()
            if is_ajax:
                return JsonResponse({
                    'success': True,
                    'review': {
                        'username': request.user.username,
                        'rating': int(rating),
                        'comment': comment,
                        'created_at': review.created_at.strftime('%b %d, %Y'),
                        'place_name': place.name,
                        'place_id': place.id
                    }
                })
            messages.success(request, "Review added successfully!")
            return redirect('state_detail', state_name=place.state.name.lower().replace(' ', '-'))
        except Exception as e:
            if is_ajax:
                return JsonResponse({'success': False, 'error': str(e)}, status=500)
            messages.error(request, "An error occurred while adding your review. Please try again.")
            return redirect('state_detail', state_name=place.state.name.lower().replace(' ', '-'))
    if is_ajax:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)
    return redirect('state_detail', state_name=place.state.name.lower().replace(' ', '-'))

@login_required
def add_favorite(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    # Add to both the ManyToMany field and the Favorite model
    place.favorited_by.add(request.user)
    Favorite.objects.get_or_create(user=request.user, place=place)
    messages.success(request, f"{place.name} added to favorites!")
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    return redirect('core:state_detail', state_slug=place.state.name.lower().replace(' ', '-'))

@login_required
def remove_favorite(request, place_id):
    if request.method == 'POST':
        try:
            place = get_object_or_404(Place, id=place_id)
            # Remove from both the ManyToMany field and the Favorite model
            place.favorited_by.remove(request.user)
            Favorite.objects.filter(user=request.user, place=place).delete()
            messages.success(request, f'Removed {place.name} from your favorites')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
        except Exception as e:
            messages.error(request, f'Error removing from favorites: {str(e)}')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': str(e)})
    return redirect('core:my_favorites')

@login_required
def add_state_favorite(request, state_id):
    state = get_object_or_404(State, id=state_id)
    state.favorites.add(request.user)
    messages.success(request, f"{state.name} added to favorites!")
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    return redirect('core:state_detail', state_slug=state.name.lower().replace(' ', '-'))

@login_required
def remove_state_favorite(request, state_id):
    state = get_object_or_404(State, id=state_id)
    state.favorites.remove(request.user)
    messages.success(request, f"{state.name} removed from favorites.")
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    return redirect('core:state_detail', state_slug=state.name.lower().replace(' ', '-'))

@login_required
def add_post_favorite(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.favorites.add(request.user)
    messages.success(request, f"{post.title} added to favorites!")
    return redirect('home')

@login_required
def remove_post_favorite(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.favorites.remove(request.user)
    messages.success(request, f"{post.title} removed from favorites!")
    return redirect('home')

@login_required
def my_favorites(request):
    # Get all places favorited by the user
    favorite_places = Place.objects.filter(favorited_by=request.user)
    
    # Get all states favorited by the user
    favorite_states = State.objects.filter(favorites=request.user)
    
    # Get weather data for each place
    places_with_weather = []
    for place in favorite_places:
        place_data = {
            'place': place,
            'weather': get_weather_data(place.location) if place.location else None,
            'latitude': place.latitude,
            'longitude': place.longitude
        }
        places_with_weather.append(place_data)
    
    context = {
        'places_with_weather': places_with_weather,
        'favorite_states': favorite_states,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'core/my_favorites.html', context)

# --- Weather API endpoint ---
def get_weather(request):
    api_key = settings.OPENWEATHERMAP_API_KEY
    city = "Chennai"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            return JsonResponse({
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'condition': data['weather'][0]['description'].capitalize(),
                'icon': data['weather'][0]['icon'],
                'wind_speed': data['wind']['speed'],
            })
    except Exception as e:
        logger.error(f"Error fetching weather data: {str(e)}")
    return JsonResponse({'error': 'Failed to fetch weather data'}, status=500)

@require_GET
def get_gemini_recommendations(request):
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')
    user_place = request.GET.get('user_place')
    place_type = request.GET.get('place_type', 'tourist_attraction')
    budget = request.GET.get('budget', 'medium')
    duration = request.GET.get('duration', 'medium')
    itinerary = request.GET.get('itinerary', 'false')
    travel_style = request.GET.get('travel_style', 'cultural')
    trip_duration = request.GET.get('trip_duration', '3')
    enhanced = request.GET.get('enhanced', 'false')
    context = request.GET.get('context', 'south_india')
    allowed_places_param = request.GET.get('allowed_places')
    allowed_places = None
    if allowed_places_param:
        try:
            allowed_places = set(json.loads(allowed_places_param))
        except Exception as e:
            logger.error(f"Failed to parse allowed_places: {e}")
            allowed_places = None

    if not all([latitude, longitude, user_place]):
        return JsonResponse({'error': 'Missing required parameters: latitude, longitude, and user_place are required.'}, status=400)

    try:
        final_recommendations = []  # Ensure always defined for error handling
        recommendations_text = ""  # Initialize to avoid scope issues
        
        # Step 1: Fetch current weather
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={settings.OPENWEATHERMAP_API_KEY}&units=metric"
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        weather_condition = weather_data['weather'][0]['main'].lower()
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        location_name = weather_data.get('name', user_place)
        weather_description = weather_data['weather'][0]['description']

        # Step 2: Get current time dynamically
        ist = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(ist).strftime('%I:%M %p IST')

        # Step 3: Construct enhanced natural language prompt for Gemini
        if itinerary == 'true':
            # Enhanced prompt for itinerary generation with more diversity
            prompt = (
                f"You are an expert travel planner specializing in {context.replace('_', ' ').title()} tourism. "
                f"The user is planning a {trip_duration}-day trip starting from '{user_place}' "
                f"with a {travel_style} travel style and {budget} budget. "
                f"Current weather: {weather_condition}, {temperature}°C, {humidity}% humidity at {current_time}.\n\n"
                f"IMPORTANT: Provide a DIVERSE mix of places. Include different types of attractions:\n"
                f"- Temples and religious sites\n"
                f"- Natural attractions (beaches, hills, parks)\n"
                f"- Historical monuments and forts\n"
                f"- Museums and cultural centers\n"
                f"- Local markets and shopping areas\n"
                f"- Hidden gems and offbeat locations\n\n"
                f"Based on the travel style '{travel_style}', suggest exactly 12-15 diverse places that would create an optimal itinerary. "
                f"Consider:\n"
                f"1. **Diversity**: Mix different types of attractions\n"
                f"2. **{travel_style.title()} Focus**: Prioritize places that match this style\n"
                f"3. **Weather Conditions**: Current {weather_condition} weather and {temperature}°C temperature\n"
                f"4. **Budget Level**: {budget} budget considerations\n"
                f"5. **Cultural Significance**: Historical and cultural importance\n"
                f"6. **Practical Logistics**: Distance, accessibility, and timing\n"
                f"7. **Local Expertise**: Include hidden gems and local favorites\n"
                f"8. **Variety**: Ensure each day has different types of experiences\n\n"
                f"Provide the response **strictly** in this format (one place per line):\n"
                f"1. Place Name - Detailed reasoning (30-50 words explaining why this place is perfect for {travel_style} travelers, considering weather, budget, and cultural significance)\n"
                f"2. Place Name - Detailed reasoning\n"
                f"3. Place Name - Detailed reasoning\n"
                f"... (continue for 12-15 diverse places)\n"
                f"Each reasoning should be specific, contextual, and actionable for the traveler. "
                f"Ensure you include a good mix of temples, beaches, hills, historical sites, and local experiences."
            )
        else:
            # Enhanced prompt for general recommendations with more diversity
            prompt = (
                f"You are a travel guide specializing in {context.replace('_', ' ').title()} tourism. "
                f"The user is currently at '{user_place}' where it's {weather_condition} with {temperature}°C "
                f"at {current_time}. They want {place_type.replace('_', ' ')}s with {budget} budget for {duration} duration.\n\n"
                f"IMPORTANT: Provide a DIVERSE mix of places. Include:\n"
                f"- Popular tourist attractions\n"
                f"- Hidden gems and local favorites\n"
                f"- Different types of experiences\n"
                f"- Places suitable for current weather\n\n"
                f"Provide exactly 8-10 diverse nearby places considering:\n"
                f"1. **Current Conditions**: {weather_condition} weather, {temperature}°C, {humidity}% humidity\n"
                f"2. **Budget Level**: {budget} budget considerations\n"
                f"3. **Duration**: {duration} visit duration\n"
                f"4. **Cultural Context**: Rich cultural and historical significance\n"
                f"5. **Local Expertise**: Include authentic local experiences\n"
                f"6. **Practical Tips**: Accessibility, crowd levels, best timing\n"
                f"7. **Variety**: Mix of different attraction types\n\n"
                f"Provide the response **strictly** in this format (one place per line):\n"
                f"1. Place Name - Comprehensive reasoning (25-40 words explaining why this place is ideal right now, considering weather, budget, duration, and cultural significance)\n"
                f"2. Place Name - Comprehensive reasoning\n"
                f"3. Place Name - Comprehensive reasoning\n"
                f"4. Place Name - Comprehensive reasoning\n"
                f"5. Place Name - Comprehensive reasoning\n"
                f"6. Place Name - Comprehensive reasoning\n"
                f"7. Place Name - Comprehensive reasoning\n"
                f"8. Place Name - Comprehensive reasoning\n"
                f"Each reasoning must be specific, contextual, and provide actionable insights for the traveler. "
                f"Ensure diversity in the types of places recommended."
            )

        # Step 4: Call Gemini API to get recommendations
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(prompt)
        
        # Log the raw response for debugging
        logger.info(f"Gemini API raw response: {response.text}")
        
        if not response or not response.text:
            raise ValueError("Empty response from Gemini API")
            
        recommendations_text = response.text

        # Parse the response with improved error handling
        recommended_places = []
        lines = recommendations_text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Skip lines that are clearly notes
            if line.lower().startswith('note:') or line.lower().startswith('important:'):
                continue
                
            try:
                # Remove numbering like "1. "
                content = line
                if '.' in line and line.split('.', 1)[0].strip().isdigit():
                    content = line.split('.', 1)[1].strip()
                
                # Try to split by " - " which is more specific, then ":"
                separator = None
                if ' - ' in content:
                    separator = ' - '
                elif ': ' in content:
                    separator = ': '
                
                if separator:
                    place_name, explanation = content.split(separator, 1)
                    place_name = place_name.strip()
                    explanation = explanation.strip()

                    if place_name and explanation:
                        recommended_places.append({
                            "name": place_name,
                            "reasoning": explanation
                        })
                else:
                    logger.warning(f"Could not parse line, no valid separator found: {line}")
                    
            except Exception as e:
                logger.warning(f"Failed to parse line: {line}. Error: {str(e)}")
                continue

        if not recommended_places:
            logger.error(f"Failed to parse any recommendations from response: {recommendations_text}")
            return JsonResponse({
                'error': 'Failed to parse recommendations from Gemini API response',
                'raw_response': recommendations_text
            }, status=500)

        # Step 5: Cross-reference with database first, then Google Maps API
        final_recommendations = []
        for place in recommended_places:
            try:
                place_name = place['name']
                
                # First, try to find the place in our database
                from .models import State, Place
                try:
                    # Get the state based on context
                    state_name = context.replace('_', ' ').title()
                    if context == 'tamil_nadu':
                        state_name = 'Tamil Nadu'
                    elif context == 'telangana':
                        state_name = 'Telangana'
                    elif context == 'andhra_pradesh':
                        state_name = 'Andhra Pradesh'
                    elif context == 'karnataka':
                        state_name = 'Karnataka'
                    elif context == 'kerala':
                        state_name = 'Kerala'
                    
                    state = State.objects.filter(name__iexact=state_name).first()
                    
                    if state:
                        # Search for the place in our database
                        db_place = Place.objects.filter(
                            state=state,
                            name__icontains=place_name
                        ).first()
                        
                        if db_place and db_place.latitude and db_place.longitude:
                            # Use the database place with accurate coordinates
                            final_recommendations.append({
                                'name': db_place.name,
                                'latitude': db_place.latitude,
                                'longitude': db_place.longitude,
                                'rating': db_place.average_rating or 0,
                                'reasoning': place['reasoning'],
                                'formatted_address': db_place.location or '',
                                'place_id': str(db_place.id),
                                'types': [db_place.category] if db_place.category else []
                            })
                            continue  # Skip Google Maps API call
                except Exception as e:
                    logger.warning(f"Database lookup failed for {place_name}: {str(e)}")
                
                # If not found in database, fall back to Google Maps API
                # Enhanced search query for better results, focusing on place name and state context
                search_query = f"{place_name}, {context.replace('_', ' ')}"
                
                # Try multiple search strategies for better accuracy
                search_queries = [
                    f"{place_name}, {context.replace('_', ' ')}",
                    f"{place_name} {context.replace('_', ' ')}",
                    f"{place_name}, Tamil Nadu" if context == 'tamil_nadu' else f"{place_name}, {context.replace('_', ' ')}",
                    place_name  # Fallback to just the place name
                ]
                
                place_found = False
                for search_query in search_queries:
                    places_url = (
                        f"https://maps.googleapis.com/maps/api/place/textsearch/json?"
                        f"query={search_query}&key={settings.GOOGLE_MAPS_API_KEY}"
                    )
                    places_response = requests.get(places_url)
                    places_response.raise_for_status()
                    places_data = places_response.json()

                    if places_data['status'] == 'OK' and places_data['results']:
                        place_details = places_data['results'][0]
                        
                        # Additional validation: check if the result is actually in the right state/region
                        formatted_address = place_details.get('formatted_address', '').lower()
                        if (context == 'tamil_nadu' and 'tamil nadu' in formatted_address) or \
                           (context == 'telangana' and 'telangana' in formatted_address) or \
                           (context == 'andhra pradesh' in formatted_address) or \
                           (context == 'karnataka' and 'karnataka' in formatted_address) or \
                           (context == 'kerala' and 'kerala' in formatted_address):
                            
                            final_recommendations.append({
                                'name': place_details.get('name', place_name),
                                'latitude': place_details['geometry']['location']['lat'],
                                'longitude': place_details['geometry']['location']['lng'],
                                'rating': place_details.get('rating', 0),
                                'reasoning': place['reasoning'],
                                'formatted_address': place_details.get('formatted_address', ''),
                                'place_id': place_details.get('place_id', ''),
                                'types': place_details.get('types', [])
                            })
                            place_found = True
                            break
                
                if not place_found:
                    logger.warning(f"Google Maps API could not find accurate location for place: {place_name}")
                    # Add the place without coordinates if Google Maps fails
                    final_recommendations.append({
                        'name': place_name,
                        'latitude': None,
                        'longitude': None,
                        'rating': 0,
                        'reasoning': place['reasoning'],
                        'formatted_address': '',
                        'place_id': '',
                        'types': []
                    })
            except Exception as e:
                logger.warning(f"Failed to get Google Maps data for {place['name']}: {str(e)}")
                # Add the place without coordinates if Google Maps fails
                final_recommendations.append({
                    'name': place['name'],
                    'latitude': None,
                    'longitude': None,
                    'rating': 0,
                    'reasoning': place['reasoning'],
                    'formatted_address': '',
                    'place_id': '',
                    'types': []
                })

        # --- FILTER BY allowed_places if provided ---
        if allowed_places:
            allowed_places_normalized = set(n.strip().lower() for n in allowed_places)
            filtered_recommendations = [p for p in final_recommendations if p['name'].strip().lower() in allowed_places_normalized]
            if filtered_recommendations:
                final_recommendations = filtered_recommendations
            # else: fallback to all results (do not filter)

        if not final_recommendations:
            logger.error("No valid places found in Google Maps")
            return JsonResponse({
                'error': 'Failed to find places in Google Maps',
                'raw_response': recommendations_text
            }, status=500)

        # Limit results based on request type
        max_places = 15 if itinerary == 'true' else 10
        # For itinerary, return as many as found (even if <12), but show a warning if very few
       
        result = {
            'gemini_recommended_places': final_recommendations[:max_places],
            'weather_data': {
                'temperature': temperature,
                'weather': weather_condition,
                'humidity': humidity,
                'description': weather_description,
                'location': location_name
            },
            'context': {
                'travel_style': travel_style,
                'budget': budget,
                'duration': duration,
                'trip_duration': trip_duration,
                'user_place': user_place
            }
        }
        cache_key = f"gemini_recommendations_{latitude}_{longitude}_{user_place}_{place_type}_{budget}_{duration}_{itinerary}_{travel_style}_{trip_duration}_{enhanced}_{context}"
        cache.set(cache_key, result, timeout=3600)
        return JsonResponse(result)

    except Exception as e:
        logger.error(f"Error in Gemini API call: {str(e)}")
        return JsonResponse({'error': f'Failed to get recommendations: {str(e)}'}, status=500)

    except requests.exceptions.RequestException as e:
        logger.error(f"API request error in get_gemini_recommendations: {str(e)}")
        return JsonResponse({'error': f'Failed to fetch data from external API: {str(e)}'}, status=500)
    except Exception as e:
        logger.error(f"Error in get_gemini_recommendations: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

def submit_inquiry(request, state_id):
    state = get_object_or_404(State, id=state_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        travel_dates = request.POST.get('travel_dates')
        travelers = request.POST.get('travelers')
        message = request.POST.get('message')
        # Validate input
        if not all([name, email, message]):
            messages.error(request, "All fields are required.")
            return redirect('state_detail', state_name=state.name.lower().replace(' ', '-'))
        # Save the inquiry
        inquiry = Inquiry(
            state=state,
            name=name,
            email=email,
            phone=phone,
            travel_dates=travel_dates,
            travelers=travelers,
            message=message,
            user=request.user if request.user.is_authenticated else None
        )
        inquiry.save()
        messages.success(request, "Your inquiry has been submitted successfully!")
        return redirect('state_detail', state_name=state.name.lower().replace(' ', '-'))
    # If not a POST request, redirect back to the state page
    return redirect('state_detail', state_name=state.name.lower().replace(' ', '-'))

def fetch_place_info(request):
    """
    API endpoint to fetch detailed information about a place using Composio.
    """
    place_name = request.GET.get('place')
    if not place_name:
        return JsonResponse({"error": "Place not provided"}, status=400)
    
    try:
        toolset = ComposioToolSet()
        result = toolset.execute_action(
            action=Action.GOOGLEMAPS_GET_PLACE_INFO,
            params={
                "place_name": place_name
            }
        )
        
        if not result.get("successful"):
            return JsonResponse({"error": result.get("error", "Failed to fetch place details")}, status=500)
            
        return JsonResponse(result.get("data", {}), safe=False)
    except Exception as e:
        logger.error(f"Error in fetch_place_info: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)

def fetch_route_info(request):
    """
    API endpoint to fetch route planning information using Composio.
    """
    origin = request.GET.get('origin')
    destination = request.GET.get('destination')
    mode = request.GET.get('mode', 'driving')
    
    if not all([origin, destination]):
        return JsonResponse({"error": "Origin and destination are required"}, status=400)
    
    try:
        toolset = ComposioToolSet()
        result = toolset.execute_action(
            action=Action.GOOGLEMAPS_GET_DIRECTIONS,
            params={
                "origin": origin,
                "destination": destination,
                "mode": mode
            }
        )
        
        if not result.get("successful"):
            return JsonResponse({"error": result.get("error", "Failed to fetch route planning")}, status=500)
            
        return JsonResponse(result.get("data", {}), safe=False)
    except Exception as e:
        logger.error(f"Error in fetch_route_info: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)

def nearby_places(request):
    """
    API endpoint to fetch nearby places using Composio.
    """
    location = request.GET.get('location')
    place_type = request.GET.get('type', 'lodging')
    
    if not location:
        return JsonResponse({"error": "Location is required"}, status=400)
    
    try:
        toolset = ComposioToolSet()
        result = toolset.execute_action(
            action=Action.GOOGLEMAPS_FIND_PLACES_NEARBY,
            params={
                "location": location,
                "radius": 5000,  # 5km radius
                "type": place_type
            }
        )
        
        if not result.get("successful"):
            return JsonResponse({"error": result.get("error", "Failed to fetch nearby places")}, status=500)
            
        return JsonResponse(result.get("data", {}), safe=False)
    except Exception as e:
        logger.error(f"Error in nearby_places: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)

@cache_page(60 * 15)
def map_view(request):
    context = {
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'core/map_view.html', context)

@cache_page(60 * 15)
def test_api_view(request):
    """View function for testing API endpoints."""
    context = {
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'core/test_api.html', context)

def fetch_github_repos(request):
    """
    Fetch GitHub repositories for the authenticated user using Composio.
    """
    try:
        toolset = ComposioToolSet()
        result = toolset.execute_action(
            action=Action.GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER,
            params={}
        )
        
        if not result.get("successful"):
            return JsonResponse({"error": result.get("error", "Failed to fetch GitHub repositories")}, status=500)
        
        return JsonResponse(result.get("data", {}), safe=False)
    except Exception as e:
        logger.error(f"Error fetching GitHub repos: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)

@login_required
def add_recommended_favorite(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            
            # Find the state based on coordinates
            state = State.objects.first()  # Default to first state for now
            
            # Create a new Place object for the recommended place
            place = Place.objects.create(
                name=name,
                latitude=latitude,
                longitude=longitude,
                description=f"Recommended place: {name}",
                state=state,
                category='recommended'  # Add a category to identify recommended places
            )
            
            # Add to user's favorites using the favorited_by field
            place.favorited_by.add(request.user)
            
            return JsonResponse({
                'success': True,
                'message': f'Added {name} to your favorites'
            })
        except Exception as e:
            logger.error(f"Error adding favorite: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    }, status=400)