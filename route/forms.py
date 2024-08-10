from django import forms
from .models import Route, NodeOrigin, NodeDestination


class RouteForm(forms.ModelForm):

    class Meta:
        model = Route
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'origin': forms.Select(attrs={'class': 'form-select'}),
            'destination': forms.Select(attrs={'class': 'form-select'}),
        }
        fields = ('origin', 'destination','description')
        

class OriginForm(forms.ModelForm):

    class Meta:
        model = NodeOrigin
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phoneNumber': forms.TextInput(attrs={'class': 'form-control'}),
        }
        fields = ('name', 'address','phoneNumber')

class DestinationForm(forms.ModelForm):

    class Meta:
        model = NodeDestination
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phoneNumber': forms.TextInput(attrs={'class': 'form-control'}),
        }
        fields = ('name', 'address','phoneNumber')
  
