from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone']
    
    name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input input-bordered w-full",
        "placeholder": "Contact name"
    }))
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "input input-bordered w-full",
        "placeholder": "Email address"
    }))
    
    phone = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input input-bordered w-full",
        "placeholder": "Phone number (optional)"
    }))