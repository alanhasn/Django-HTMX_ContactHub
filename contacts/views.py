from django.shortcuts import render
from .models import Contact , User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import ContactForm
from django.views.decorators.http import require_http_methods


# Create your views here.
@login_required
def index(request):
    contacts = request.user.contacts.all().order_by('id')
    context = {
        'contacts': contacts,
        'form':ContactForm
    }
    return render(request, 'contacts.html', context)

@login_required
def search_contacts(request):
    """
        Search contacts based on name or email.
    """
    import time
    time.sleep(1)
    query = request.GET.get("search") # This is the query parameter from the request

    contacts = request.user.contacts.filter(
        Q(name__icontains=query) | Q(email__icontains=query) # Using Q objects for complex queries
    )
    return render(request , "partials/contact_list.html" , context={"contacts":contacts}) # This will render the contact list with the filtered contacts

@login_required
@require_http_methods(["POST"])
def create_contact(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        contact = form.save(commit=False)
        contact.user = request.user
        contact.save()
        
        context = {"contact":contact}
        response =  render(request , "partials/add-contact-row.html" , context=context)
        response["HX-Trigger"] = "success"
        return response