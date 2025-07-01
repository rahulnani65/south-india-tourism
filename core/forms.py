from django import forms
from .models import UserProfile, State
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = UserProfile
        fields = ['bio', 'phone_number', 'location', 'travel_style', 'favorite_state']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tell us about yourself and your travel experiences...'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 98765 43210'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your current location'}),
            'travel_style': forms.Select(choices=[
                ('', 'Select your travel style'),
                ('adventure', 'Adventure Seeker'),
                ('relaxation', 'Relaxation & Wellness'),
                ('cultural', 'Cultural Explorer'),
                ('luxury', 'Luxury Traveler'),
                ('budget', 'Budget Traveler'),
                ('family', 'Family Traveler'),
                ('solo', 'Solo Traveler'),
                ('photography', 'Photography Enthusiast'),
                ('foodie', 'Food & Culinary'),
            ], attrs={'class': 'form-control'}),
            'favorite_state': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial values for user fields
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
        
        # Populate favorite_state choices
        self.fields['favorite_state'].queryset = State.objects.all()
        self.fields['favorite_state'].empty_label = "Select your favorite state"
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        
        # Update user fields
        if self.instance and self.instance.user:
            user = self.instance.user
            user.first_name = self.cleaned_data.get('first_name', '')
            user.last_name = self.cleaned_data.get('last_name', '')
            user.email = self.cleaned_data.get('email', '')
            user.save()
        
        if commit:
            profile.save()
        return profile
    