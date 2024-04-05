from django.utils import timezone
from datetime import datetime
import json
import logging
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseServerError
from django.shortcuts import get_object_or_404, render, redirect
import razorpay
from .forms import MovieForm, NewUserForm, RatingForm, ShowForm, TheaterForm
from django.contrib.auth import login, authenticate 
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .models import Movie, Rating, RazorPayment, Show, Theater, Ticket, Seat, User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache

# Create your views here.
def home(request):
    return render(request,'home.html')

from .forms import NewUserForm
from django.contrib import messages

def register_user(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "You have registered successfully.")
            return redirect("book_movie:login")
    else:
        form = NewUserForm()
    
    # If form is not valid or it's a GET request, render the registration form with errors (if any)
    return render(request, "register.html", {"register_form": form})


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"You are now logged in as {username}.")
                return redirect("book_movie:movie_list")
            else:
                # Authentication failed due to invalid username or password
                messages.error(request, "Invalid username or password.")
        else:
            # Form validation failed due to missing or invalid fields
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"login_form": form})

@never_cache
def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("book_movie:login")

@login_required
def movie_list(request):
    movies=Movie.objects.all()
    return render(request,'movie_list.html',{'movies':movies})

@login_required
def movie_details(request,movie_id):
    movie=Movie.objects.get(pk=movie_id)
    return render(request, 'movie_detail.html', {'movie': movie})

@login_required
def movie_show(request, movie_id):
    movie=Movie.objects.get(pk=movie_id)
    movie_show=Show.objects.filter(movie_id=movie_id)  #collect movie shows of selected movie
    theater_list=set(show.Theater_name for show in movie_show)   #get theater list of show of selected movie
    
    theater_with_show = {}  #dictionary like map in cpp
    for theater in theater_list:
        theater_with_show[theater]=movie_show.filter(Theater_name=theater)  #give movie_show to their theater
    return render(request, 'movie_show.html', {'movie':movie, 'theater_with_show':theater_with_show})

@login_required
def seat_map(request, Show_id): 
    try:
        show = Show.objects.get(Show_id=Show_id) # or pk
    except Show.DoesNotExist:
        return HttpResponse("Show not found", status=404)
    tickets = Ticket.objects.filter(Show_id=show.Show_id)
    ticket_numbers = [tk.ticket_no for tk in tickets]
    seats = Seat.objects.filter(ticket_no__in=ticket_numbers) 
    num = {1, 2, 3, 4, 5, 6, 7, 8, 9} 
    
    request.session['show_id']=show.Show_id
    request.session['show_price']=show.ticket_price
    
    return render(request, "seat_map.html", {'seats' : seats, 'num' : num})



client = razorpay.Client(auth=('rzp_test_yRDb0bPGUsE0lL', '56dX6KIdE0sSWX4U55F8j3lj'))

@login_required
def payment_page(request):
    show_price=request.session.get('show_price')
    
    selected_seats_str = request.POST.get('selectedSeatsStr')
    request.session['selected_seats_str']=selected_seats_str
    selected_seats_list = json.loads(selected_seats_str)  # Convert JSON string to Python list
    number_of_seats = len(selected_seats_list)
    total_amount=number_of_seats*show_price
    DATA = {
        "amount": total_amount*100,
        "currency": "INR",
        "payment_capture":1
    }
    payment_order=client.order.create(data=DATA)
    payment_order_id=payment_order['id']

    context = {
            'api_key':'rzp_test_yRDb0bPGUsE0lL',
            'order_id':payment_order_id,
            'selected_seats' : selected_seats_str,
            'amount' : total_amount
        }
    return render(request, 'pay.html', context)    
    
@login_required
def book_successfully(request):
    if request.method == "POST":
        selected_seats_str = request.session.get('selected_seats_str')
        Show_id=request.session.get('show_id')
        show = Show.objects.get(Show_id=Show_id)
        show_price=show.ticket_price
        selected_seats_list = json.loads(selected_seats_str)
        number_of_seats = len(selected_seats_list)
        if(number_of_seats == 0):
            print(1234)
        if(show_price == 0):
            print(5678)
        total_amount=number_of_seats*show_price
        user = request.user
        user_ticket = Ticket.objects.create(
            user=user,
            Show_id=show,
            amount=float(total_amount)
        )
        
        # Convert the string representation of selected seats into a list of seat positions
        # selected_seats_list = selected_seats_str.strip("[]").split(',"')
        # Create Seat objects for each selected seat position
        seats = []
        for seat_position in selected_seats_list:
            row, col = seat_position.split("-")
            seat = Seat.objects.create(
                ticket_no=user_ticket,  # Assuming this field can be null
                seat_row=row,
                seat_col=col,
                is_booked=True
            )
            seats.append(seat)
        
        return render(request, "book_successfully.html", {'selected_seats' : selected_seats_str, 'total_amount' : total_amount})
    else:
        # Handle other HTTP methods if necessary
        # For example, if you only expect POST requests, you can return a 405 Method Not Allowed response
        return HttpResponseNotAllowed(['POST'])

@login_required
# add movie
def add_movie(request):
    movie_form = MovieForm(request.POST, request.FILES)  
    if movie_form.is_valid():
        movie = movie_form.save(commit=False)  
        if 'image' in request.FILES: 
            movie.image = request.FILES['image']  
        movie.save() 
        return redirect("book_movie:movie_list")
    else:
        movie_form = MovieForm()
    return render(request, 'add_movie.html', {'movie_form': movie_form})

@login_required
def update_movie(request, id):
    movie_obj = get_object_or_404(Movie, movie_id=id)
    movie_form = MovieForm(instance=movie_obj)
    return render(request, "update_movie.html", {"movie_form": movie_form})

@login_required
def updated_movie(request, id):
    movie_obj = get_object_or_404(Movie, movie_id=id)
    movie_form = MovieForm(request.POST,request.FILES, instance=movie_obj)
    if movie_form.is_valid():
        movie_form.save()
        return redirect("/movie_details/"+str(id))  
    return render(request, "update_movie.html", {"movie_form": movie_form})

@login_required
def delete_movie(request, id):
    context ={}
    obj = get_object_or_404(Movie, movie_id = id)
    if request.method =="POST":
        obj.delete()
        return redirect("/movie/")
    return render(request, "delete_movie.html", context)

# @login_required
# def theater_list(request):
#     theaters=Theater.objects.all()
#     return render(request,'theater_list.html',{'theaters':theaters})
def book(request,movie_id):
  
        today = timezone.localdate()
        shows = Show.objects.filter(movie_id=movie_id, Show_date__gte=today).order_by('Show_date')
        return render(request, 'theater_list.html', {'shows': shows,'movie_id': movie_id})

@login_required
def theater_details(request, pk):
    theater_obj = get_object_or_404(Theater, Theater_name=pk)
    return render(request, 'theater_details.html', {'theater': theater_obj})

@login_required
def theater_list_admin(request):
    theaters=Theater.objects.all()
    return render(request,'theater_list_admin.html',{'theaters':theaters})

@login_required
def theater_list(request,movie_id):
    selected_date = request.GET.get('selected_date')

    if not selected_date:
        selected_date = timezone.localdate()

    # Convert selected_date to a datetime object for comparison
    selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()

    # Get the current time if the selected date is today
    if selected_date == timezone.localdate():
        current_time = datetime.now().time()
    else:
        # If the selected date is a future date, set current_time to None
        current_time = None

    # Filter shows based on the selected date and movie_id
    shows_on_selected_date = Show.objects.filter(Show_date=selected_date, movie_id=movie_id)

    # Filter out the shows that have already passed if selected_date is today
    if current_time:
        shows_on_selected_date = shows_on_selected_date.filter(start_time__gte=current_time)

    # Extract theater IDs from the filtered shows
    theater_ids = shows_on_selected_date.values_list('Theater_name_id', flat=True)

    # Filter theaters based on the extracted theater IDs
    theaters = Theater.objects.filter(Theater_name__in=theater_ids)
    return render(request, 'theater_list.html', {'theaters': theaters, 'shows': shows_on_selected_date,'movie_id':movie_id})
    # return render(request,'theater_list.html',{'theaters':theaters,'shows': shows_on_selected_date,'movie_id':movie_id})

@login_required
# after click edit button in theater_list for admin 
def update_Theater(request,id):
    user=User.objects.get(pk=id)
    Theater_obj = get_object_or_404(Theater, user=user)
    Theater_form = TheaterForm(instance=Theater_obj)
    return render(request, "update_Theater.html", {"Theater_form": Theater_form})

@login_required
def updated_Theater(request, id):
    user=User.objects.get(pk=id)
    Theater_obj = get_object_or_404(Theater, user=user)
    Theater_form = TheaterForm(request.POST or None,instance=Theater_obj)
    if Theater_form.is_valid():
        Theater_form.save()
        return redirect("/movie/theater_list/")  
    return render(request, "update_Theater.html", {"Theater_form": Theater_form})

@login_required
# delete the theater from list
def delete_Theater(request, id):
    context ={}
    obj = get_object_or_404(Theater, user_id = id)
    if request.method =="POST":
        obj.delete()
        return redirect("/movie/theater_list/")
    return render(request, "delete_theater.html", context)

# @login_required
# # add the theater in list
# def add_Theater(request):
#     theater = TheaterForm(request.POST)  
#     if theater.is_valid():
#         theater1=theater.save(commit=False)
#         theater1.user=request.user
#         theater1.save()
#         # return redirect("book_movie:theater_list_admin")
#     else:
#         theater = TheaterForm()
#     return render(request, 'add_theater.html', {'theater': theater})

def add_Theater(request):
    if request.method == 'POST':
        theater_form = TheaterForm(request.POST)
        if theater_form.is_valid():
            theater = theater_form.save(commit=False)
            theater.user = request.user  # Assign the current user to the theater
            theater.save()
            return redirect("book_movie:theater_list_admin")
        else:
            # Retrieve theaters associated with the current user
            user_theaters = Theater.objects.filter(user=request.user)

            # Filter the list of users to include only the currently logged-in user
            user_choices = [(request.user.id, request.user.username)]

            # Update the user field choices in the form
            theater_form = TheaterForm(initial={'user': request.user.id})
            theater_form.fields['user'].choices = user_choices
            return render(request, 'add_theater.html', {'theater_form': theater_form, 'user_theaters': user_theaters})
    
    return redirect("book_movie:theater_list_admin")

@login_required
def show_list(request):
    movie_show=Show.objects.all()  #collect movie shows of selected movie
    theater_list=set(show.Theater_name for show in movie_show)   #get theater list of show of selected movie
    
    theater_with_show = {}  #dictionary like map in cpp
    for theater in theater_list:
        theater_with_show[theater]=movie_show.filter(Theater_name=theater)
    return render(request,'show_list.html',{'theater_with_show':theater_with_show})

@login_required
def show_details(request,id):
    show = get_object_or_404(Show, Show_id=id)
    # show = ShowForm()
    return render(request,'show_details.html',{'show':show})

@login_required
def update_show(request,id):
    show_obj = get_object_or_404(Show, Show_id=id)
    show_form = ShowForm(instance=show_obj)
    return render(request, "update_show.html", {"show_form": show_form})

@login_required
def updated_show(request, id):
    show_obj = get_object_or_404(Show, Show_id=id)
    show_form = ShowForm(request.POST or None,instance=show_obj)
    if show_form.is_valid():
        show_form.save()
        return redirect("/movie/show_list/")  
    return render(request, "update_show.html", {"show_form": show_form})

@login_required
def delete_show(request, id):
    context ={}
    obj = get_object_or_404(Show, Show_id = id)
    if request.method =="POST":
        obj.delete()
        return redirect("/movie/show_list/")
    return render(request, "delete_show.html", context)

@login_required
def add_show(request):
    if request.method == "POST": 
        show = ShowForm(request.POST) 
        if show.is_valid():
            show_obj=show.save() 
            return redirect('book_movie:show_details', id=show_obj.Show_id)
    else:
        show = ShowForm()
    return render(request, 'add_show.html', {'show': show})


@login_required
def rating(request):
    ratings=Rating.objects.all()
    return render(request,'rating.html',{'ratings':ratings})

@login_required
def add_rating(request):
    data = {}
    rating = RatingForm(request.POST)
    if rating.is_valid():
        rating.save()
        data['rating'] = rating
        return redirect("book_movie:rating")
    else:
        rating = RatingForm()
        return render(request,'add_rating.html',{'rating':rating})
    
@login_required  
def my_booking(request):
    user=request.user
    tickets=Ticket.objects.filter(user=user)
    return render(request, 'my_booking.html', {'tickets':tickets})

@login_required
def full_ticket(request, ticket_no):
    ticket= Ticket.objects.get(ticket_no=ticket_no)
    seats= Seat.objects.filter(ticket_no=ticket_no)
    return render(request, 'full_ticket.html', {'ticket':ticket, 'seats':seats})