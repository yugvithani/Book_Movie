from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from book_movie.models import Movie, Rating, RazorPayment, Show, Theater

# Create your forms here.

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = [
        "movie_title",
        "img",
        "description",
        "cast",
        "grade",
        "movie_type",
        "release_date",
        "duration",
        "rating",
        ]

    # def save(self, commit=True):
    #     user = super(MovieForm, self).save(commit=False)
    #     user.movie_title = self.cleaned_data['movie_title']
    #     user.img = self.cleaned_data['img']
    #     user.description = self.cleaned_data['description']
    #     user.cast = self.cleaned_data['cast']
    #     user.grade = self.cleaned_data['grade']
    #     user.movie_type = self.cleaned_data['movie_type']
    #     user.release_date = self.cleaned_data['release_date']
    #     user.duration = self.cleaned_data['duration']
    #     user.rating = self.cleaned_data['rating']
    #     if commit:
    #         user.save()
    #     return user
   


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = [
        "review",
        "rating",
        ]
    def clean_rating(self):
            rating = self.cleaned_data['rating']
            if rating < 1 or rating > 5:
                raise forms.ValidationError("Rating must be between 1 and 5.")
            return rating
    # def save(self, commit=True):
    #     user = super(RatingForm, self).save(commit=False)
    #     user.review = self.cleaned_data['review']
    #     user.rating = self.cleaned_data['rating']
    #     if commit:
    #         user.save()
    #     return user
   
class TheaterForm(forms.ModelForm):
    class Meta:
        model = Theater
        fields =[
            "Theater_name",
            "city",
            "address",
            "total_screens",
            "user",
        ]
        error_messages = {
            'Theater_name': {'required': ""},
            'city': {'required': ""},
            'address': {'required': ""},
            'total_screens': {'required': ""},
            'user': {'required': ""},
        }

class ShowForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = [
            "Show_id", 
            "movie_id",
            "Theater_name", 
            "start_time", 
            "end_time", 
            "Show_date",     
            "Screen_no",
            "ticket_price"
        ]
        
# MoviePayment form
class RazorPaymentForm(forms.ModelForm):
    class Meta:
        model = RazorPayment
        fields = ['name', 'email','amount']
