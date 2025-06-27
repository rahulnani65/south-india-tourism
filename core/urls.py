from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('state/get-gemini-recommendations/', views.get_gemini_recommendations, name='get_gemini_recommendations'),
    path('state/<str:state_slug>/', views.state_detail, name='state_detail'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('profile/ai-analysis/', views.get_ai_personality_analysis, name='ai_personality_analysis'),
    path('profile/travel-recommendations/', views.get_travel_recommendations, name='travel_recommendations'),
    path('profile/bucket-list/', views.update_bucket_list, name='update_bucket_list'),
    path('profile/travel-stats/', views.get_travel_stats, name='travel_stats'),
    path('add-review/<int:place_id>/', views.add_review, name='add_review'),
    path('add-favorite/<int:place_id>/', views.add_favorite, name='add_favorite'),
    path('remove-favorite/<int:place_id>/', views.remove_favorite, name='remove_favorite'),
    path('add-recommended-favorite/', views.add_recommended_favorite, name='add_recommended_favorite'),
    path('add-state-favorite/<int:state_id>/', views.add_state_favorite, name='add_state_favorite'),
    path('remove-state-favorite/<int:state_id>/', views.remove_state_favorite, name='remove_state_favorite'),
    path('add-post-favorite/<int:post_id>/', views.add_post_favorite, name='add_post_favorite'),
    path('remove-post-favorite/<int:post_id>/', views.remove_post_favorite, name='remove_post_favorite'),
    path('my-favorites/', views.my_favorites, name='my_favorites'),
    path('weather/', views.get_weather, name='get_weather'),
    path('submit-inquiry/<int:state_id>/', views.submit_inquiry, name='submit_inquiry'),
    path('api/place-details/', views.fetch_place_info, name='fetch_place_info'),
    path('api/route-info/', views.fetch_route_info, name='fetch_route_info'),
    path('test-api/', views.test_api_view, name='test_api'),
    path('api/github/repos/', views.fetch_github_repos, name='github_repos'),
    path('map/', views.map_view, name='map_view'),
]