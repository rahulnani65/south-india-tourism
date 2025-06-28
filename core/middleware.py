from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class NoCacheMiddleware:
    """Middleware to prevent caching of pages"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Add no-cache headers to all responses
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        
        # Add security headers
        response['X-Frame-Options'] = 'DENY'
        response['X-Content-Type-Options'] = 'nosniff'
        
        return response

class LoginRequiredMiddleware:
    """Middleware to handle login requirements for specific views"""
    def __init__(self, get_response):
        self.get_response = get_response
        # Define paths that require login
        self.login_required_paths = [
            '/state/',
            '/post/',
            '/contact/submit/',
            '/profile/',
            '/my-favorites/',
            '/weather/',
            '/map/',
            '/test-api/',
            '/api/',
            '/favorite/',
            '/review/',
        ]

    def __call__(self, request):
        # Check if the current path requires login
        path_requires_login = any(request.path.startswith(path) for path in self.login_required_paths)
        
        # Skip for login and signup pages
        if request.path in ['/login/', '/signup/']:
            return self.get_response(request)
        
        # If path requires login and user is not authenticated
        if path_requires_login and not request.user.is_authenticated:
            # Store the intended destination
            request.session['next'] = request.get_full_path()
            
            # Add a message to inform the user
            messages.warning(request, 'Please log in to access this feature.')
            
            # Redirect to login page
            return redirect('login')
        
        response = self.get_response(request)
        return response