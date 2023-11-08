from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,logout # Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from .models import Offer
from .forms import OfferForm
from django.db.models import Q
from datetime import datetime
# Create your views here.

def home(request):
    all_offers = Offer.objects.all()
    offers_per_page = 2  # Adjust this to your desired number

    paginator = Paginator(all_offers, offers_per_page)
    page = request.GET.get('page')

    try:
        offers = paginator.page(page)
    except PageNotAnInteger:
        # If the 'page' parameter is not an integer, display the first page.
        offers = paginator.page(1)
    except EmptyPage:
        # If the 'page' parameter is out of range, display the last page.
        offers = paginator.page(paginator.num_pages)

    return render(request, 'home.html', {'all_offers': offers})
def SignUp(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if pass1!=pass2:
            return HttpResponse("Your Password1  and password2 are not same.")
        else:
            my_user = User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('SignIn')
    return render(request, 'SignUp.html')

def SignIn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1= request.POST.get('password1')
        print(username,password1)
        user=authenticate(request,username=username,password=password1)
        
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            print(username,password1)
            return HttpResponse("Password is incorrect")
        
    return render(request,'SignIn.html')

def logoutpage(request):
    logout(request)
    return redirect('SignIn')

@login_required
def create_offer(request):
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.user = request.user
            offer.save()
            return redirect('home')
    else:
        form = OfferForm()
    return render(request,'create_offer.html',{'form':form})

def remove(request,id):
    item = Offer.objects.get(id=id)
    item.delete()
    return redirect('home')

def edit(request,id):
    offer = get_object_or_404(Offer, id=id)

    if request.method == 'POST':
        form = OfferForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()  # Save the updated employee information
            return redirect('home')  # Redirect to the list of employees

    else:
        form = OfferForm(instance=offer)

    return render(request, 'edit.html', {'form': form, 'offer': offer})

def filter_offers(request):
    query = request.GET.get('q')
    user_query = request.GET.get('user')
    mytype_query = request.GET.get('mytype')
    start_date_query = request.GET.get('start_date')
    end_date_query = request.GET.get('end_date')

    # Initial queryset
    offers = Offer.objects.all()

    if query:
        # Apply filters based on the query
        offers = offers.filter(
            Q(user__username__icontains=query) |
            Q(mytype__name__icontains=query) |
            Q(start_date__icontains=query) |
            Q(end_date__icontains=query)
        )

    if user_query:
        # Filter by user username
        offers = offers.filter(user__username__icontains=user_query)

    if mytype_query:
        # Filter by offer type name
        offers = offers.filter(mytype__name__icontains=mytype_query)

    if start_date_query:
        # Filter by start date
        offers = offers.filter(start_date__icontains=start_date_query)

    if end_date_query:
        # Filter by end date
        offers = offers.filter(end_date__icontains=end_date_query)

    return render(request, 'filter_offers.html', {'all_offers': offers})

