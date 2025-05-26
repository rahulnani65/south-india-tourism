from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('state/<str:state_slug>/', views.state_detail, name='state_detail'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('add-review/<int:place_id>/', views.add_review, name='add_review'),
    path('add-favorite/<int:place_id>/', views.add_favorite, name='add_favorite'),
    path('remove-favorite/<int:place_id>/', views.remove_favorite, name='remove_favorite'),
    path('add-state-favorite/<int:state_id>/', views.add_state_favorite, name='add_state_favorite'),
    path('remove-state-favorite/<int:state_id>/', views.remove_state_favorite, name='remove_state_favorite'),
    path('add-post-favorite/<int:post_id>/', views.add_post_favorite, name='add_post_favorite'),
    path('remove-post-favorite/<int:post_id>/', views.remove_post_favorite, name='remove_post_favorite'),
    path('my-favorites/', views.my_favorites, name='my_favorites'),
    path('get-weather/', views.get_weather, name='get_weather'),
    path('get-recommendations/', views.get_recommendations, name='get_recommendations'),
    path('submit-inquiry/<int:state_id>/', views.submit_inquiry, name='submit_inquiry'),
]