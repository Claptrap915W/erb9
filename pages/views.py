from django.shortcuts import render
from listings.models import Listing
from listings.choices import district_choices, room_type_choices, rooms_choices
#from django.http import HttpResponse

# def index(request):
#     return HttpResponse("<h1>Hello, World !</h1>")
# Create your views here.

def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)[:3]
    context = {"listings" : listings, "district_choices": district_choices, 
    "room_type_choices":room_type_choices,"rooms_choices":rooms_choices}
    return render(request, "pages/index.html", context)

def about(request):
    return render(request, "pages/about.html")