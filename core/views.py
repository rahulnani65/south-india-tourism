import requests
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout as auth_logout
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
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from .models import Cuisine, Restaurant
from django.db.models import Q
import re

logger = logging.getLogger(__name__)

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

def no_cache_response(view_func):
    """Decorator to add no-cache headers to responses"""
    def wrapper(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    return wrapper

@no_cache_response
def home(request):
    """Home page view with enhanced caching and performance"""
    try:
        # Get featured states
        states = State.objects.all()[:5]
        
        # Get featured places
        featured_places = Place.objects.filter(is_featured=True)[:6]
        
        # Get recent reviews
        recent_reviews = Review.objects.select_related('user', 'place').order_by('-created_at')[:3]
        
        # Get cuisine data
        cuisines = Cuisine.objects.all()[:4]
        
        # Check if user is authenticated
        is_authenticated = request.user.is_authenticated
        
        # Get user-specific data if authenticated
        user_favorites = []
        if is_authenticated:
            user_favorites = Favorite.objects.filter(user=request.user).select_related('place')[:3]
        
        context = {
            'states': states,
            'featured_places': featured_places,
            'recent_reviews': recent_reviews,
            'cuisines': cuisines,
            'is_authenticated': is_authenticated,
            'user_favorites': user_favorites,
        }
        
        return render(request, 'core/index.html', context)
        
    except Exception as e:
        logger.error(f"Error in home view: {str(e)}")
        # Return a basic context if there's an error
        return render(request, 'core/index.html', {})

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
            'is_favorite': place.favorited_by.filter(id=request.user.id).exists(),
            'image_url': place.image_url or ''
        }
        places_with_weather.append(place_data)
    
    # Check if the state is in user's favorites
    is_state_favorite = state.favorites.filter(id=request.user.id).exists()
    
    context = {
        'state': state,
        'places_with_weather': places_with_weather,
        'hotels': hotels,
        'reviews': reviews,
        'itineraries': itineraries,
        'transport_options': transport_options,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
        'is_state_favorite': is_state_favorite
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

@login_required
@cache_page(60 * 15)
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    is_favorited = post.favorites.filter(id=request.user.id).exists()
    return render(request, 'core/post_detail.html', {'post': post, 'is_favorited': is_favorited})

@login_required
def contact_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')  # Default to empty string if not provided
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Only save phone if it's not empty
        contact_data = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message
        }
        
        if phone.strip():  # Only add phone if it's not empty
            contact_data['phone'] = phone
            
        Contact.objects.create(**contact_data)
        messages.success(request, "Your message has been sent successfully!")
        return redirect('home')
    return redirect('home')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                # Log the user in immediately after signup
                login(request, user)
                
                # Create a UserProfile for the new user
                try:
                    UserProfile.objects.create(user=user)
                except:
                    pass  # Profile might already exist
                
                messages.success(request, f'Welcome {user.username}! Your account has been created successfully. You are now logged in.')
                
                # Redirect to home page with cache-busting
                response = redirect('home')
                response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private, max-age=0'
                response['Pragma'] = 'no-cache'
                response['Expires'] = '0'
                
                # Add cache-busting parameter
                import time
                cache_buster = int(time.time())
                response['Location'] = f'/?cb={cache_buster}'
                
                return response
            except Exception as e:
                logger.error(f"Error during signup: {str(e)}")
                messages.error(request, 'An error occurred during account creation. Please try again.')
        else:
            # Handle form validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, error)
                    else:
                        field_name = form.fields[field].label if field in form.fields else field
                        messages.error(request, f"{field_name}: {error}")
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile(request):
    # Ensure the user has a UserProfile, create one if it doesn't exist
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    # Update user statistics
    user_profile.update_stats()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('core:profile')
    else:
        form = UserProfileForm(instance=user_profile)

    # Get travel level
    travel_level = user_profile.get_travel_level()

    # Get recent reviews
    recent_reviews = Review.objects.filter(user=request.user).select_related('place').order_by('-created_at')[:5]

    # Get recent favorites
    recent_favorites = Favorite.objects.filter(user=request.user).select_related('place').order_by('-created_at')[:5]

    # Get timeline events (recent activities)
    timeline_events = []
    
    # Add recent reviews to timeline
    for review in recent_reviews[:3]:
        timeline_events.append({
            'title': f'Reviewed {review.place.name}',
            'description': f'Gave {review.rating} stars',
            'date': review.created_at,
            'icon': 'star'
        })
    
    # Add recent favorites to timeline
    for favorite in recent_favorites[:3]:
        timeline_events.append({
            'title': f'Added {favorite.place.name} to favorites',
            'description': f'Added to your bucket list',
            'date': favorite.created_at,
            'icon': 'heart'
        })

    # Sort timeline events by date
    timeline_events.sort(key=lambda x: x['date'], reverse=True)

    context = {
        'form': form,
        'user_profile': user_profile,
        'travel_level': travel_level,
        'timeline_events': timeline_events,
        'recent_reviews': recent_reviews,
        'recent_favorites': [favorite.place for favorite in recent_favorites],
    }
    
    return render(request, 'core/profile.html', context)

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

@login_required
def get_weather(request):
    """Get weather data for a specific location"""
    if request.method == 'GET':
        location = request.GET.get('location')
        if location:
            weather_data = get_weather_data(location)
            if weather_data:
                return JsonResponse(weather_data)
            else:
                return JsonResponse({'error': 'Unable to fetch weather data'}, status=400)
        else:
            return JsonResponse({'error': 'Location parameter is required'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
@require_GET
def get_gemini_recommendations(request):
    """Get AI-powered travel recommendations using Gemini"""
    try:
        # Extract parameters from GET request
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')
        user_place = request.GET.get('user_place')
        place_type = request.GET.get('place_type', 'tourist_attraction')
        budget = request.GET.get('budget', 'medium')
        duration = request.GET.get('duration', 'medium')
        context = request.GET.get('context', 'south_india')

        # Optionally, fetch weather data (if you want to keep it)
        weather_condition = None
        temperature = None
        humidity = None
        location_name = user_place
        weather_description = None
        if latitude and longitude:
            try:
                weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={settings.OPENWEATHERMAP_API_KEY}&units=metric"
                weather_response = requests.get(weather_url)
                weather_response.raise_for_status()
                weather_data = weather_response.json()
                weather_condition = weather_data['weather'][0]['main'].lower()
                temperature = weather_data['main']['temp']
                humidity = weather_data['main']['humidity']
                location_name = weather_data.get('name', user_place)
                weather_description = weather_data['weather'][0]['description']
            except Exception as e:
                logger.warning(f"Weather API failed: {e}")

        # Build the Gemini prompt using label inputs
        prompt = f"""
        You are a travel expert for {context.replace('_', ' ').title()}. The user is currently at '{user_place}' and wants recommendations for {place_type.replace('_', ' ')}s with a {budget} budget for a {duration} visit.
        """
        if weather_condition and temperature:
            prompt += f" The current weather is {weather_condition} with a temperature of {temperature}°C."
        prompt += f"\n\nPlease provide 5-7 diverse and interesting places in {context.replace('_', ' ')} that match these criteria. For each place, include:\n- name (string)\n- reasoning (string, 1-2 sentences on why it's a good fit for the user's preferences)\n- best_time (string)\n- budget_range (string)\n- tips (string)\n- latitude (float, if known)\n- longitude (float, if known)\n\nRespond ONLY with a valid JSON array. Do NOT include any comments (// ...) or explanations outside the JSON."

        # Generate response using Gemini
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(prompt)
        
        def clean_gemini_json(text):
            # Remove triple backticks and optional language tag (e.g., ```json)
            text = text.strip()
            if text.startswith('```'):
                # Remove the first line (``` or ```json)
                text = text.split('\n', 1)[-1]
            if text.endswith('```'):
                text = text.rsplit('```', 1)[0]
            return text.strip()

        cleaned_response = remove_json_comments(response.text)
        cleaned_response = clean_gemini_json(cleaned_response)
        try:
            places = json.loads(cleaned_response)
        except Exception as e:
            logger.error(f"Failed to parse Gemini response as JSON: {e}\nGemini response: {response.text}")
            return JsonResponse({
                'error': 'Failed to parse recommendations from Gemini API response',
                'raw_gemini_response': response.text
            }, status=500)

        # Optionally, include weather data in the response
        weather_info = None
        if weather_condition and temperature:
            weather_info = {
                'temperature': temperature,
                'weather': weather_condition,
                'humidity': humidity,
                'description': weather_description,
                'location': location_name
            }

        return JsonResponse({
            'gemini_recommended_places': places,
            'weather_data': weather_info,
            'context': {
                'user_place': user_place,
                'place_type': place_type,
                'budget': budget,
                'duration': duration,
                'context': context
            }
        })
            
    except Exception as e:
        logger.error(f"Error generating Gemini recommendations: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Failed to generate recommendations'
        }, status=500)

@login_required
def submit_inquiry(request, state_id):
    state = get_object_or_404(State, id=state_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        if name and email and message:
            Inquiry.objects.create(
                state=state,
                name=name,
                email=email,
                message=message
            )
            messages.success(request, f'Your inquiry about {state.name} has been submitted successfully!')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return redirect('core:state_detail', state_slug=state.name.lower().replace(' ', '-'))

@login_required
def fetch_place_info(request):
    """Fetch detailed information about a place"""
    if request.method == 'GET':
        place_id = request.GET.get('place_id')
        if place_id:
            try:
                place = Place.objects.get(id=place_id)
                return JsonResponse({
                    'name': place.name,
                    'description': place.description,
                    'location': place.location,
                    'category': place.category,
                    'average_rating': place.average_rating or 0,
                    'image_url': place.image_url or '',
                    'latitude': place.latitude,
                    'longitude': place.longitude
                })
            except Place.DoesNotExist:
                return JsonResponse({'error': 'Place not found'}, status=404)
        else:
            return JsonResponse({'error': 'Place ID is required'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def fetch_route_info(request):
    """Fetch route information between two places"""
    if request.method == 'GET':
        origin = request.GET.get('origin')
        destination = request.GET.get('destination')
        
        if not origin or not destination:
            return JsonResponse({'error': 'Origin and destination are required'}, status=400)
        
        # This would typically call Google Maps Directions API
        # For now, return a placeholder response
        return JsonResponse({
            'origin': origin,
            'destination': destination,
            'distance': '25 km',
            'duration': '45 minutes',
            'route_type': 'driving'
        })
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def nearby_places(request):
    """Get nearby places based on coordinates"""
    if request.method == 'GET':
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        radius = request.GET.get('radius', 10)  # Default 10km radius
        
        if not lat or not lng:
            return JsonResponse({'error': 'Latitude and longitude are required'}, status=400)
        
        try:
            # Find places within the specified radius
            places = Place.objects.filter(
                latitude__isnull=False,
                longitude__isnull=False
            )[:10]  # Limit to 10 places
            
            nearby_places_data = []
            for place in places:
                nearby_places_data.append({
                    'id': place.id,
                    'name': place.name,
                    'category': place.category,
                    'latitude': place.latitude,
                    'longitude': place.longitude,
                    'average_rating': place.average_rating or 0
                })
            
            return JsonResponse({'places': nearby_places_data})
            
        except Exception as e:
            logger.error(f"Error fetching nearby places: {str(e)}")
            return JsonResponse({'error': 'Failed to fetch nearby places'}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
@cache_page(60 * 15)
def map_view(request):
    """Interactive map view"""
    states = State.objects.all()
    places = Place.objects.filter(latitude__isnull=False, longitude__isnull=False)[:50]
    
    context = {
        'states': states,
        'places': places,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'core/map_view.html', context)

@login_required
@cache_page(60 * 15)
def test_api_view(request):
    """Test API endpoint"""
    return JsonResponse({'status': 'success', 'message': 'API is working correctly'})

@login_required
def fetch_github_repos(request):
    """Fetch GitHub repositories (placeholder for future integration)"""
    return JsonResponse({
        'repositories': [
            {'name': 'South India Tourism', 'description': 'Tourism website for South India'},
            {'name': 'Travel API', 'description': 'API for travel recommendations'}
        ]
    })

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

@login_required
def get_ai_personality_analysis(request):
    """
    Get AI-powered personality analysis for travel recommendations.
    """
    try:
        # Get user's profile and preferences
        user_profile = request.user.profile
        user_favorites = Favorite.objects.filter(user=request.user)
        
        # Analyze user's travel preferences based on their favorites
        favorite_places = [fav.place for fav in user_favorites]
        favorite_states = [fav.place.state for fav in user_favorites if fav.place.state]
        
        # Create a comprehensive personality analysis
        personality_traits = []
        travel_motivation = "Exploration and discovery"
        personalized_message = "Keep exploring the beautiful South India!"
        travel_insights = ""
        preferred_experiences = []
        travel_strengths = []
        
        # Analyze based on number of favorites
        if len(user_favorites) > 10:
            personality_traits.append('Travel Expert')
            travel_motivation = "Deep cultural immersion and authentic experiences"
            personalized_message = "You're a seasoned traveler! Consider exploring hidden gems and offbeat destinations."
            travel_strengths.extend(['Experience', 'Cultural Awareness', 'Adaptability'])
        elif len(user_favorites) > 5:
            personality_traits.append('Travel Enthusiast')
            travel_motivation = "Adventure and new experiences"
            personalized_message = "You love exploring! Try visiting different types of destinations to broaden your horizons."
            travel_strengths.extend(['Curiosity', 'Open-mindedness', 'Adventure Spirit'])
        elif len(user_favorites) > 2:
            personality_traits.append('Travel Explorer')
            travel_motivation = "Learning and discovery"
            personalized_message = "You're developing your travel style! Explore more destinations to find your preferences."
            travel_strengths.extend(['Learning Mindset', 'Exploration'])
        else:
            personality_traits.append('Travel Beginner')
            travel_motivation = "New experiences and cultural exposure"
            personalized_message = "Welcome to the world of travel! Start with popular destinations and gradually explore more."
            travel_strengths.extend(['Fresh Perspective', 'Eagerness to Learn'])
        
        # Analyze based on favorite categories
        favorite_categories = [place.category for place in favorite_places if place.category]
        if favorite_categories:
            category_counts = {}
            for category in favorite_categories:
                category_counts[category] = category_counts.get(category, 0) + 1
            
            most_liked_category = max(category_counts, key=category_counts.get)
            
            if most_liked_category == 'temple':
                personality_traits.append('Spiritual Explorer')
                preferred_experiences.extend(['Temple visits', 'Cultural ceremonies', 'Meditation retreats'])
                travel_insights = "You appreciate spiritual and cultural experiences. Consider visiting ancient temples and participating in local rituals."
            elif most_liked_category == 'beach':
                personality_traits.append('Nature Lover')
                preferred_experiences.extend(['Beach activities', 'Water sports', 'Sunset watching'])
                travel_insights = "You enjoy natural beauty and relaxation. Explore more coastal destinations and nature reserves."
            elif most_liked_category == 'fort':
                personality_traits.append('History Buff')
                preferred_experiences.extend(['Historical tours', 'Museum visits', 'Heritage walks'])
                travel_insights = "You're fascinated by history and architecture. Visit more historical monuments and heritage sites."
            elif most_liked_category == 'park':
                personality_traits.append('Adventure Seeker')
                preferred_experiences.extend(['Outdoor activities', 'Wildlife spotting', 'Adventure sports'])
                travel_insights = "You love outdoor adventures and wildlife. Try trekking, wildlife safaris, and adventure activities."
        
        # Analyze based on favorite states
        if favorite_states:
            state_names = [state.name for state in favorite_states if state]
            if len(set(state_names)) > 2:
                personality_traits.append('Multi-State Explorer')
                travel_insights += " You enjoy exploring different states and cultures."
            else:
                personality_traits.append('Focused Explorer')
                travel_insights += " You prefer to explore destinations in depth."
        
        # Remove duplicates and create final analysis
        personality_traits = list(set(personality_traits))
        preferred_experiences = list(set(preferred_experiences))
        travel_strengths = list(set(travel_strengths))
        
        analysis = {
            'personality_type': ' & '.join(personality_traits) if personality_traits else 'Travel Enthusiast',
            'travel_motivation': travel_motivation,
            'personalized_message': personalized_message,
            'travel_insights': travel_insights,
            'preferred_experiences': preferred_experiences,
            'travel_strengths': travel_strengths,
            'total_favorites': len(user_favorites),
            'favorite_categories': list(set(favorite_categories)),
            'preferred_states': list(set([state.name for state in favorite_states if state]))
        }
        
        return JsonResponse({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        logger.error(f"Error in AI personality analysis: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Failed to generate personality analysis'
        }, status=500)

@login_required
def get_travel_recommendations(request):
    """
    Get personalized travel recommendations based on user preferences.
    """
    try:
        user_profile = request.user.profile
        user_favorites = Favorite.objects.filter(user=request.user)
        
        # Get user's favorite places and states
        favorite_places = [fav.place for fav in user_favorites]
        favorite_states = [fav.place.state for fav in user_favorites if fav.place.state]
        
        # Generate recommendations based on preferences
        recommendations = []
        
        # Recommend places from states they haven't visited
        all_states = State.objects.all()
        visited_states = set([state.name for state in favorite_states if state])
        
        for state in all_states:
            if state.name not in visited_states:
                state_places = Place.objects.filter(state=state)[:3]
                for place in state_places:
                    recommendations.append({
                        'name': place.name,
                        'state': state.name,
                        'description': place.description[:100] + '...' if len(place.description) > 100 else place.description,
                        'best_time': 'Year-round',
                        'estimated_cost': f'₹{place.entry_fee or 500}',
                        'category': place.category,
                        'type': 'new_state'
                    })
        
        # Recommend similar places based on categories
        favorite_categories = [place.category for place in favorite_places if place.category]
        if favorite_categories:
            most_liked_category = max(set(favorite_categories), key=favorite_categories.count)
            similar_places = Place.objects.filter(category=most_liked_category).exclude(
                id__in=[place.id for place in favorite_places]
            )[:5]
            
            for place in similar_places:
                recommendations.append({
                    'name': place.name,
                    'state': place.state.name,
                    'description': place.description[:100] + '...' if len(place.description) > 100 else place.description,
                    'best_time': 'Year-round',
                    'estimated_cost': f'₹{place.entry_fee or 500}',
                    'category': place.category,
                    'type': 'similar_places'
                })
        
        # If no recommendations based on preferences, suggest popular places
        if not recommendations:
            popular_places = Place.objects.all()[:10]
            for place in popular_places:
                recommendations.append({
                    'name': place.name,
                    'state': place.state.name,
                    'description': place.description[:100] + '...' if len(place.description) > 100 else place.description,
                    'best_time': 'Year-round',
                    'estimated_cost': f'₹{place.entry_fee or 500}',
                    'category': place.category,
                    'type': 'popular'
                })
        
        return JsonResponse({
            'success': True,
            'recommendations': {
                'recommendations': recommendations[:8]  # Limit to 8 recommendations
            }
        })
        
    except Exception as e:
        logger.error(f"Error generating travel recommendations: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Failed to generate recommendations'
        }, status=500)

@login_required
def update_bucket_list(request):
    """
    Update user's bucket list (places they want to visit).
    """
    if request.method == 'POST':
        try:
            # Handle both JSON and form data
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                # Handle form-encoded data
                data = request.POST
            
            action = data.get('action')  # 'add' or 'remove'
            item = data.get('item', '').strip()
            
            if not item:
                return JsonResponse({
                    'success': False,
                    'error': 'Item is required'
                }, status=400)
            
            user_profile = request.user.profile
            
            if action == 'add':
                # Add to bucket list if not already present
                if item not in user_profile.travel_bucket_list:
                    user_profile.travel_bucket_list.append(item)
                    user_profile.save()
                    message = f'Added "{item}" to your bucket list'
                else:
                    return JsonResponse({
                        'success': False,
                        'error': 'Item already in bucket list'
                    }, status=400)
                    
            elif action == 'remove':
                # Remove from bucket list
                if item in user_profile.travel_bucket_list:
                    user_profile.travel_bucket_list.remove(item)
                    user_profile.save()
                    message = f'Removed "{item}" from your bucket list'
                else:
                    return JsonResponse({
                        'success': False,
                        'error': 'Item not found in bucket list'
                    }, status=400)
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid action'
                }, status=400)
            
            return JsonResponse({
                'success': True,
                'message': message,
                'bucket_list': user_profile.travel_bucket_list
            })
            
        except Exception as e:
            logger.error(f"Error updating bucket list: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': 'Failed to update bucket list'
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    }, status=400)

@login_required
def get_travel_stats(request):
    """
    Get user's travel statistics and achievements.
    """
    try:
        user_favorites = Favorite.objects.filter(user=request.user)
        user_reviews = Review.objects.filter(user=request.user)
        
        # Calculate statistics
        stats = {
            'total_favorites': len(user_favorites),
            'total_reviews': len(user_reviews),
            'states_visited': len(set([fav.state.name for fav in user_favorites if hasattr(fav, 'state') and fav.state])),
            'average_rating': 0,
            'favorite_categories': {},
            'recent_activity': []
        }
        
        # Calculate average rating
        if user_reviews:
            total_rating = sum(review.rating for review in user_reviews)
            stats['average_rating'] = round(total_rating / len(user_reviews), 1)
        
        # Get favorite categories
        favorite_places = [fav.place for fav in user_favorites]
        for place in favorite_places:
            if place.category:
                stats['favorite_categories'][place.category] = stats['favorite_categories'].get(place.category, 0) + 1
        
        # Get recent activity (last 5 favorites and reviews)
        recent_favorites = user_favorites.order_by('-created_at')[:5]
        recent_reviews = user_reviews.order_by('-created_at')[:5]
        
        for fav in recent_favorites:
            stats['recent_activity'].append({
                'type': 'favorite',
                'place': fav.place.name,
                'date': fav.created_at.strftime('%Y-%m-%d'),
                'time_ago': timesince(fav.created_at)
            })
        
        for review in recent_reviews:
            stats['recent_activity'].append({
                'type': 'review',
                'place': review.place.name,
                'rating': review.rating,
                'date': review.created_at.strftime('%Y-%m-%d'),
                'time_ago': timesince(review.created_at)
            })
        
        # Sort recent activity by date
        stats['recent_activity'].sort(key=lambda x: x['date'], reverse=True)
        stats['recent_activity'] = stats['recent_activity'][:10]  # Keep only 10 most recent
        
        return JsonResponse(stats)
        
    except Exception as e:
        logger.error(f"Error getting travel stats: {str(e)}")
        return JsonResponse({'error': 'Failed to get travel statistics'}, status=500)

def custom_logout(request):
    # Debug: Log the current user before logout
    print(f"Logging out user: {request.user}")
    print(f"User is authenticated: {request.user.is_authenticated}")
    
    # Clear all session data
    request.session.flush()
    request.session.delete()
    
    # Logout the user
    auth_logout(request)
    
    # Debug: Check if user is still authenticated
    print(f"After logout - User: {request.user}")
    print(f"After logout - User is authenticated: {request.user.is_authenticated}")
    
    # Add a success message
    messages.success(request, 'You have been successfully logged out.')
    
    # Redirect to home page with cache-busting parameters
    response = redirect('home')
    
    # Clear any authentication cookies
    response.delete_cookie('sessionid')
    response.delete_cookie('csrftoken')
    response.delete_cookie('auth_token')
    
    # Add aggressive cache control headers to prevent caching
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    response['X-Frame-Options'] = 'DENY'
    response['X-Content-Type-Options'] = 'nosniff'
    
    # Add cache-busting parameter to URL
    import time
    cache_buster = int(time.time())
    response['Location'] = f'/?cb={cache_buster}'
    
    return response

def auth_status(request):
    """Debug view to check authentication status"""
    return JsonResponse({
        'user': str(request.user),
        'is_authenticated': request.user.is_authenticated,
        'session_id': request.session.session_key,
        'session_data': dict(request.session.items())
    })

def custom_login(request):
    """Custom login view with better error handling and notifications"""
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'Please provide both username and password.')
            return render(request, 'registration/login.html')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}! You have been successfully logged in.')
            
            # Redirect to next parameter or home
            next_url = request.POST.get('next', 'home')
            if next_url == '':
                next_url = 'home'
            
            response = redirect(next_url)
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            
            return response
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    
    return render(request, 'registration/login.html')

def remove_json_comments(text):
    # Remove // ... comments
    return re.sub(r'//.*', '', text)

def clean_gemini_json(text):
    # Remove triple backticks and optional language tag (e.g., ```json)
    text = text.strip()
    if text.startswith('```'):
        # Remove the first line (``` or ```json)
        text = text.split('\n', 1)[-1]
    if text.endswith('```'):
        text = text.rsplit('```', 1)[0]
    return text.strip()

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        auth_logout(request)
        user.delete()
        return redirect('home')
    return render(request, 'registration/delete_account_confirm.html')