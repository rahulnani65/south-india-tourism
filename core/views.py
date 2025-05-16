from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import State, Contact, Hotel, Place, UserProfile, Favorite, Review

def home(request):
    states = State.objects.all()
    return render(request, 'core/index.html', {'states': states})

def state_detail(request, state_name):
    state = get_object_or_404(State, name__iexact=state_name.replace('-', ' '))
    places = state.places.all()

    # Handle category filter
    category = request.GET.get('category', '')
    if category:
        places = places.filter(category=category)

    # Prepare places with hotels and reviews
    places_with_hotels = []
    for place in places:
        near_hotels = place.hotels.filter(distance__lte=5)
        place.hotels_near = near_hotels
        place.reviews_list = place.reviews.all()[:3]
        # Check if the place is favorited by the current user
        place.is_favorited = request.user.is_authenticated and place.favorited_by.filter(user=request.user).exists()
        places_with_hotels.append(place)

    # Prepare suggested itinerary (static for now)
    itinerary = [
        {"day": 1, "activity": f"Visit {places[0].name} in the morning, explore nearby areas in the afternoon."} if places else {"day": 1, "activity": "Explore the state capital or major city."},
        {"day": 2, "activity": "Discover cultural sites and enjoy local cuisine."},
        {"day": 3, "activity": "Relax at a beach or natural spot, then depart."},
    ]

    # Local transportation options (static for now)
    transport_options = [
        {"mode": "Public Bus", "details": "Affordable, covers major tourist spots."},
        {"mode": "Taxi", "details": "Convenient for short trips, approx. $10-20 per ride."},
        {"mode": "Rental Car", "details": "Flexible, daily rates around $30-50."},
    ]

    # Check if the state is favorited by the current user
    is_favorited = request.user.is_authenticated and state.favorites.filter(id=request.user.id).exists()

    return render(request, 'core/state.html', {
        'state': state,
        'places': places_with_hotels,
        'categories': Place.CATEGORY_CHOICES,
        'selected_category': category,
        'itinerary': itinerary,
        'transport_options': transport_options,
        'is_favorited': is_favorited,  # For state favorites
    })

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
        return redirect('home')
    return redirect('home')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'registration/signup.html', {'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

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
    return redirect('state_detail', state_name=place.state.name.lower().replace(' ', '-'))

@login_required
def add_favorite(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    Favorite.objects.get_or_create(user=request.user, place=place)
    return redirect('state_detail', state_name=place.state.name.lower().replace(' ', '-'))

@login_required
def remove_favorite(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    Favorite.objects.filter(user=request.user, place=place).delete()
    return redirect('state_detail', state_name=place.state.name.lower().replace(' ', '-'))

@login_required
def add_state_favorite(request, state_id):
    state = get_object_or_404(State, id=state_id)
    state.favorites.add(request.user)
    return redirect('state_detail', state_name=state.name.lower().replace(' ', '-'))

@login_required
def remove_state_favorite(request, state_id):
    state = get_object_or_404(State, id=state_id)
    state.favorites.remove(request.user)
    return redirect('state_detail', state_name=state.name.lower().replace(' ', '-'))

@login_required
def my_favorites(request):
    # Get favorited places
    favorite_places = Place.objects.filter(favorited_by__user=request.user)
    # Get favorited states
    favorite_states = State.objects.filter(favorites=request.user)
    return render(request, 'core/favorites.html', {
        'favorite_places': favorite_places,
        'favorite_states': favorite_states,
    })