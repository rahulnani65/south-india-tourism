from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import State, Contact, Hotel, Place, UserProfile, Favorite, Review, Post, Itinerary, TransportationOption
from .forms import UserProfileForm

def home(request):
    states = State.objects.all()
    posts = Post.objects.all().order_by('-created_at')[:3]
    return render(request, 'core/index.html', {'states': states, 'posts': posts})

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
        place.is_favorited = request.user.is_authenticated and place.favorited_by.filter(user=request.user).exists()
        places_with_hotels.append(place)

    # Fetch itinerary and transportation options
    itinerary = state.itineraries.all()
    transport_options = state.transport_options.all()

    # Check if the state is favorited by the current user
    is_favorited = request.user.is_authenticated and state.favorites.filter(id=request.user.id).exists()

    return render(request, 'core/state.html', {
        'state': state,
        'places': places_with_hotels,
        'categories': Place.CATEGORY_CHOICES,
        'selected_category': category,
        'itinerary': itinerary,
        'transport_options': transport_options,
        'is_favorited': is_favorited,
    })

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
    return redirect('state_detail', state_name=place.state.name.lower().replace(' ', '-'))

@login_required
def add_favorite(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    Favorite.objects.get_or_create(user=request.user, place=place)
    messages.success(request, f"{place.name} added to favorites!")
    return redirect('state_detail', state_name=place.state.name.lower().replace(' ', '-'))

@login_required
def remove_favorite(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    Favorite.objects.filter(user=request.user, place=place).delete()
    messages.success(request, f"{place.name} removed from favorites!")
    return redirect('state_detail', state_name=place.state.name.lower().replace(' ', '-'))

@login_required
def add_state_favorite(request, state_id):
    state = get_object_or_404(State, id=state_id)
    state.favorites.add(request.user)
    messages.success(request, f"{state.name} added to favorites!")
    return redirect('state_detail', state_name=state.name.lower().replace(' ', '-'))

@login_required
def remove_state_favorite(request, state_id):
    state = get_object_or_404(State, id=state_id)
    state.favorites.remove(request.user)
    messages.success(request, f"{state.name} removed from favorites!")
    return redirect('state_detail', state_name=state.name.lower().replace(' ', '-'))

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