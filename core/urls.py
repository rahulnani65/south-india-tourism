# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('state/<str:state_name>/', views.state_detail, name='state_detail'),
    path('contact/', views.contact_submit, name='contact_submit'),
    # Add this for the hotel addition (optional for now)
    # path('add-hotel/', views.add_hotel, name='add_hotel'),
]