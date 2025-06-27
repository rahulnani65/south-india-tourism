from django.contrib import admin
from django.urls import path, include
from core import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('', include('core.urls')),
    path('state/<str:state_name>/', views.state_detail, name='state_detail'),
    path('contact_submit/', views.contact_submit, name='contact_submit'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.custom_logout, name='logout'),
    path('auth-status/', views.auth_status, name='auth_status'),
    path('favorite/add/<int:place_id>/', views.add_favorite, name='add_favorite'),
    path('favorite/remove/<int:place_id>/', views.remove_favorite, name='remove_favorite'),
    path('review/add/<int:place_id>/', views.add_review, name='add_review'),
]