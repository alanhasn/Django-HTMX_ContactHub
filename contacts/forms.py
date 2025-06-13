from django import forms
from .models import Contact
from django.core.exceptions import ValidationError

# Define a form class based on the Contact model
class ContactForm(forms.ModelForm):

    # Override the initializer to accept an extra 'user' argument
    def __init__(self, *args, **kwargs):
        # Pop 'user' from the keyword arguments if it exists, and store it for later use
        self.user = kwargs.pop('user', None)
        # Call the parent class's __init__ to initialize the form normally
        super().__init__(*args, **kwargs)

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

    # Define a custom validator for the email field
    def clean_email(self):

         # Get the cleaned value of the 'email' field after default validation
        email = self.cleaned_data.get("email")

        # Check if a Contact with this email already exists for the current user
        if self.user and Contact.objects.filter(user=self.user,email=email).exists():
            raise ValidationError(" This email is already in use.")
        
        return email
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if name.startswith('X'):
            raise ValidationError("No names beginning with X!")
        return name 

    def save(self, commit=True):
        contact = super().save(commit=False)
        contact.user = self.user
        if Contact.objects.filter(user=self.user, email=contact.email).exists():
            raise ValidationError("Duplicate contact for this user.")
        if commit:
            contact.save()
        return contact