from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('state/<str:state_name>/', views.state_detail, name='state_detail'),
    path('contact/', views.contact_submit, name='contact_submit'),
    path('signup/', views.signup, name='signup'),
    path('place/<int:place_id>/add-review/', views.add_review, name='add_review'),
    path('place/<int:place_id>/add-favorite/', views.add_favorite, name='add_favorite'),
    path('place/<int:place_id>/remove-favorite/', views.remove_favorite, name='remove_favorite'),
    path('state/<int:state_id>/add-favorite/', views.add_state_favorite, name='add_state_favorite'),
    path('state/<int:state_id>/remove-favorite/', views.remove_state_favorite, name='remove_state_favorite'),
    path('my-favorites/', views.my_favorites, name='my_favorites'),
]
