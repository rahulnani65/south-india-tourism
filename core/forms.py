from django import forms
from .models import UserProfile
import json

class UserProfileForm(forms.ModelForm):
    preferred_categories = forms.MultipleChoiceField(
        choices=[
            ('historical', 'Historical'),
            ('cultural', 'Cultural'),
            ('natural', 'Natural'),
            ('adventure', 'Adventure'),
            ('religious', 'Religious'),
        ],
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = UserProfile
        fields = ['preferred_categories', 'budget_preference', 'travel_style']
        widgets = {
            'budget_preference': forms.Select(choices=[
                ('low', 'Low Budget'),
                ('medium', 'Medium Budget'),
                ('high', 'High Budget'),
            ], attrs={'class': 'form-control'}),
            'travel_style': forms.Select(choices=[
                ('adventure', 'Adventure'),
                ('relaxation', 'Relaxation'),
                ('cultural', 'Cultural'),
                ('luxury', 'Luxury'),
            ], attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.preferred_categories:
            try:
                # Convert JSON string to list for initial data
                initial_categories = json.loads(self.instance.preferred_categories)
                self.initial['preferred_categories'] = initial_categories
            except (json.JSONDecodeError, TypeError):
                self.initial['preferred_categories'] = []

    def clean_preferred_categories(self):
        categories = self.cleaned_data.get('preferred_categories')
        if categories:
            return json.dumps(list(categories))
        return json.dumps([])
    