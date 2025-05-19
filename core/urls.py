from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('state/<str:state_name>/', views.state_detail, name='state_detail'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('contact/', views.contact_submit, name='contact_submit'),
    path('signup/', views.signup, name='signup'),
    path('place/<int:place_id>/add-review/', views.add_review, name='add_review'),
    path('place/<int:place_id>/add-favorite/', views.add_favorite, name='add_favorite'),
    path('place/<int:place_id>/remove-favorite/', views.remove_favorite, name='remove_favorite'),
    path('state/<int:state_id>/add-favorite/', views.add_state_favorite, name='add_state_favorite'),
    path('state/<int:state_id>/remove-favorite/', views.remove_state_favorite, name='remove_state_favorite'),
    path('post/<int:post_id>/add-favorite/', views.add_post_favorite, name='add_post_favorite'),
    path('post/<int:post_id>/remove-favorite/', views.remove_post_favorite, name='remove_post_favorite'),
    path('my-favorites/', views.my_favorites, name='my_favorites'),
    path('profile/', views.profile, name='profile'),
    # path('api/weather/', views.get_weather, name='get_weather'),
    # path('api/recommendations/', views.get_recommendations, name='get_recommendations'),
]