from django import forms
from .models import Restaurant

class RestaurantForm(forms.ModelForm):
    #to create link
    class Meta:
        model = Restaurant
        fields='__all__'
        # do the same things
        # fields = ['name', 'description', 'opening_time', 'closing_time']
