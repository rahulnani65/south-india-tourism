import requests
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count
from .models import State, Contact, Hotel, Place, UserProfile, Favorite, Review, Post, Itinerary, TransportationOption, Inquiry
from .forms import UserProfileForm
from django.conf import settings


def home(request):
    states = State.objects.all()
    posts = Post.objects.all().order_by('-created_at')[:3]
    return render(request, 'core/index.html', {'states': states, 'posts': posts})

def state_detail(request, state_slug):
    state = get_object_or_404(State, name__iexact=state_slug.replace('-', ' '))
    places = Place.objects.filter(state=state)
    hotels = Hotel.objects.filter(place__state=state)
    reviews = Review.objects.filter(place__state=state).order_by('-created_on')[:5]
    itineraries = Itinerary.objects.filter(state=state).order_by('day')
    transport_options = TransportationOption.objects.filter(state=state)
    
    # Get the template name based on the state
    template_name = f'core/states/{state.name.lower().replace(" ", "_")}.html'
    
    # If state-specific template doesn't exist, use the default state template
    if not os.path.exists(os.path.join(settings.BASE_DIR, 'core', 'templates', template_name)):
        template_name = 'core/state.html'
    
    # Get weather data for the state's main city
    weather_data = None
    if state.name == 'Andhra Pradesh':
        weather_data = get_weather_data('Visakhapatnam')
    elif state.name == 'Tamil Nadu':
        weather_data = get_weather_data('Chennai')
    elif state.name == 'Kerala':
        weather_data = get_weather_data('Kochi')
    elif state.name == 'Karnataka':
        weather_data = get_weather_data('Bangalore')
    elif state.name == 'Telangana':
        weather_data = get_weather_data('Hyderabad')
    
    context = {
        'state': state,
        'places': places,
        'hotels': hotels,
        'reviews': reviews,
        'itineraries': itineraries,
        'transport_options': transport_options,
        'weather_data': weather_data,
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
            }
            suggestions = []
            safety_tips = []
            temp = weather_data['temperature']
            condition = weather_data['condition'].lower()
            
            if "rain" in condition:
                suggestions.append(f"It's raining in {city}—visit indoor attractions.")
                safety_tips.append("Avoid coastal areas due to potential flooding.")
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
    favorite_places = Place.objects.filter(favorited_by__user=request.user)
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
        user_favorites = Place.objects.filter(favorited_by__user=request.user)
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