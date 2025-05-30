from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['preferred_categories', 'budget_preference', 'travel_style']
        widgets = {
            'preferred_categories': forms.CheckboxSelectMultiple(),
            'budget_preference': forms.Select(choices=[
                ('low', 'Low Budget'),
                ('medium', 'Medium Budget'),
                ('high', 'High Budget'),
            ]),
            'travel_style': forms.Select(choices=[
                ('adventure', 'Adventure'),
                ('relaxation', 'Relaxation'),
                ('cultural', 'Cultural'),
                ('luxury', 'Luxury'),
            ]),
        }