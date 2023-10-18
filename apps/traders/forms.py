from django import forms

class DateForm(forms.Form):
    start = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'custom-input'}, format='%Y-%m-%dT%H:%M')
    )
    end = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'custom-input'}, format='%Y-%m-%dT%H:%M')
    )
