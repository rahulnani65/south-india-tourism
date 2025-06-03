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
from composio_openai import ComposioToolSet, Action
from .composio_utils import get_place_details, get_route_planning
import logging

logger = logging.getLogger(__name__)

def home(request):
    states = State.objects.all()
    posts = Post.objects.all().order_by('-created_at')[:3]
    return render(request, 'core/index.html', {'states': states, 'posts': posts})

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
            'weather': get_weather_data(place.location) if place.location else None
        }
        places_with_weather.append(place_data)
    
    context = {
        'state': state,
        'places_with_weather': places_with_weather,
        'hotels': hotels,
        'reviews': reviews,
        'itineraries': itineraries,
        'transport_options': transport_options,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, template_name, context)

def get_weather_data(city):
    api_key = "0b8486e199e0b1fc6fd9897e7190f88c"  # Your OpenWeatherMap API key
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
        print(f"Error fetching weather data: {e}")
    return None

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

@login_required
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
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'core/profile.html', {'form': form})

@login_required
def add_review(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        Review.objects.create(
            user=request.user,
            place=place,
            rating=rating,
            comment=comment
        )
        messages.success(request, "Review added successfully!")
    return redirect('state_detail', state_slug=place.state.name.lower().replace(' ', '-'))

@login_required
def add_favorite(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    Favorite.objects.get_or_create(user=request.user, place=place)
    messages.success(request, f"{place.name} added to favorites!")
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    return redirect('state_detail', state_slug=place.state.name.lower().replace(' ', '-'))

@login_required
def remove_favorite(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    Favorite.objects.filter(user=request.user, place=place).delete()
    messages.success(request, f"{place.name} removed from favorites!")
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    return redirect('state_detail', state_slug=place.state.name.lower().replace(' ', '-'))

@login_required
def add_state_favorite(request, state_id):
    state = get_object_or_404(State, id=state_id)
    state.favorites.add(request.user)
    messages.success(request, f"{state.name} added to favorites!")
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    return redirect('state_detail', state_slug=state.name.lower().replace(' ', '-'))

@login_required
def remove_state_favorite(request, state_id):
    state = get_object_or_404(State, id=state_id)
    state.favorites.remove(request.user)
    messages.success(request, f"{state.name} removed from favorites!")
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    return redirect('state_detail', state_slug=state.name.lower().replace(' ', '-'))

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
    favorite_places = Place.objects.filter(favorited_by=request.user)
    favorite_states = State.objects.filter(favorites=request.user)
    return render(request, 'core/favorites.html', {
        'favorite_places': favorite_places,
        'favorite_states': favorite_states,
    })

# --- Weather API endpoint ---
def get_weather(request):
    api_key = "0b8486e199e0b1fc6fd9897e7190f88c"  # Your OpenWeatherMap API key
    city = "Chennai"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            weather_data = {
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'condition': data['weather'][0]['description'].capitalize(),
            }
            suggestions = []
            safety_tips = []
            temp = weather_data['temperature']
            condition = weather_data['condition'].lower()
            if "rain" in condition:
                suggestions.append("It's raining in Chennai—visit indoor attractions like the Government Museum.")
                safety_tips.append("Avoid coastal areas like Marina Beach due to potential flooding.")
            elif temp > 30:
                suggestions.append("It's hot today—stay hydrated and visit shaded spots like Guindy National Park.")
                safety_tips.append("Wear sunscreen and light clothing to protect against the heat.")
            else:
                suggestions.append("It's a pleasant day—perfect for a walk along Marina Beach!")
                safety_tips.append("Keep an eye on your belongings in crowded areas.")
            return JsonResponse({
                'success': True,
                'weather': weather_data,
                'suggestions': suggestions,
                'safety_tips': safety_tips,
            })
        else:
            return JsonResponse({'success': False, 'error': 'Unable to fetch weather data'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

# --- Recommendations endpoint ---
def get_recommendations(request):
    state_slug = request.GET.get('state_slug')
    state = get_object_or_404(State, slug=state_slug)
    places = Place.objects.filter(state=state)
    preferred_category = None
    if request.user.is_authenticated:
        user_favorites = Place.objects.filter(favorited_by=request.user)
        if user_favorites.exists():
            categories = user_favorites.values('category').annotate(count=Count('category')).order_by('-count')
            if categories:
                preferred_category = categories[0]['category']
    if preferred_category:
        recommended_places = places.filter(category=preferred_category)[:3]
    else:
        recommended_places = places.filter(category='historical')[:3]
    recommendations = [
        {
            'name': place.name,
            'category': place.category,
            'description': place.description,
        }
        for place in recommended_places
    ]
    return JsonResponse({'success': True, 'recommendations': recommendations})


def submit_inquiry(request, state_id):
    state = get_object_or_404(State, id=state_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Validate input
        if not all([name, email, message]):
            messages.error(request, "All fields are required.")
            return redirect('state_detail', state_slug=state.name.lower().replace(' ', '-'))
        # Save the inquiry
        inquiry = Inquiry(
            state=state,
            name=name,
            email=email,
            message=message,
            user=request.user if request.user.is_authenticated else None
        )
        inquiry.save()
        messages.success(request, "Your inquiry has been submitted successfully!")
        return redirect('state_detail', state_slug=state.name.lower().replace(' ', '-'))
    # If not a POST request, redirect back to the state page
    return redirect('state_detail', state_slug=state.name.lower().replace(' ', '-'))

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
        data = get_route_planning(origin, destination, mode)
        if "error" in data:
            return JsonResponse({"error": data["error"]}, status=500)
        return JsonResponse(data)
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
        url = 'https://api.composio.dev/v1/agents/invoke'
        headers = {
            'Authorization': f'Bearer {settings.COMPOSIO_API_KEY}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        payload = {
            "agent_id": "google-maps-agent",
            "action": "find_places_nearby",
            "parameters": {
                "location": location,
                "radius": 5000,  # 5km radius
                "type": place_type
            }
        }
        
        logger.info(f"Making request to Composio API for nearby places around {location}")
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        logger.info(f"Successfully received response from Composio API")
        return JsonResponse(data)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching nearby places: {str(e)}")
        return JsonResponse({"error": f"Failed to fetch nearby places: {str(e)}"}, status=500)
    except Exception as e:
        logger.error(f"Unexpected error in nearby_places: {str(e)}")
        return JsonResponse({"error": f"Unexpected error: {str(e)}"}, status=500)

def map_view(request):
    context = {
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'core/map_view.html', context)

def fetch_place_info(request):
    """
    API endpoint to fetch detailed information about a place.
    """
    place_name = request.GET.get('place')
    if not place_name:
        return JsonResponse({"error": "Place not provided"}, status=400)
    
    try:
        data = get_place_details(place_name)
        if "error" in data:
            return JsonResponse({"error": data["error"]}, status=500)
        return JsonResponse(data)
    except Exception as e:
        logger.error(f"Error in fetch_place_info: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)

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
        tools = toolset.get_tools(actions=[Action.GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER])
        
        if not tools:
            return JsonResponse({"error": "GitHub tool not found"}, status=404)
        
        # Get the first tool and ensure it's callable
        github_tool = tools[0]
        if not hasattr(github_tool, 'run'):
            return JsonResponse({"error": "GitHub tool does not have run method"}, status=500)
        
        # Run the GitHub tool with empty parameters
        result = github_tool.run({})
        
        # Check if the result is valid
        if not result:
            return JsonResponse({"error": "No repositories found"}, status=404)
            
        return JsonResponse(result, safe=False)
    
    except Exception as e:
        logger.error(f"Error fetching GitHub repos: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)