from django.db import models
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError

class Theater(models.Model):
    Theater_name = models.CharField(max_length=50, primary_key=True)
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=150)
    total_screens = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='theaters')

    def __str__(self):
        return self.Theater_name

class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    movie_title = models.CharField(max_length=100)
    img = models.ImageField(upload_to='movie_poster')
    description = models.CharField(max_length=1000)
    cast = models.CharField(max_length=255)
    grade = models.CharField(max_length=3)
    movie_type = models.CharField(max_length=30)
    release_date = models.DateField('%d-%m-%Y')
    duration = models.CharField(max_length=30)
    rating = models.FloatField(default=0)

    def __str__(self):
        return f"{self.movie_title} ({self.release_date.year})"

class Show(models.Model):
    Show_id = models.AutoField(primary_key=True)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_show')
    Theater_name = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='Theater_show')
    start_time = models.TimeField()
    end_time = models.TimeField()
    Show_date = models.DateField('%d-%m-%Y')
    Screen_no = models.PositiveIntegerField()
    ticket_price=models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f"{self.movie_id} - {self.Show_date} ({self.start_time} - {self.end_time})"

    def clean(self):
        super().clean()
        if self.Screen_no > self.Theater_name.total_screens:
            raise ValidationError("Screen number exceeds total screens in the theater.")

    def save(self, *args, **kwargs):
        self.clean()  # Validate before saving
        super().save(*args, **kwargs)

        

class Ticket(models.Model):
    BOOKING_STATUS = (
        ('BOOKED', 'BOOKED'),
        ('CANCELED', 'CANCELED')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Show_id = models.ForeignKey(Show, on_delete=models.CASCADE)
    ticket_no = models.AutoField(primary_key=True)    #
    booking_status = models.CharField(max_length=24, null=True, choices=BOOKING_STATUS, default=BOOKING_STATUS[0][0]) #
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class Seat(models.Model):
    ticket_no = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    seat_row = models.PositiveIntegerField()
    seat_col = models.PositiveIntegerField()
    is_booked = models.BooleanField(default = False)

class RazorPayment(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    amount = models.IntegerField()
    order_id=models.CharField(max_length=100,blank=True)
    razor_payment_id=models.CharField(max_length=100,blank=True)
    paid=models.BooleanField(default=False)
    def _str_(self):
        return f"Payment - {self.amount}"

class Rating(models.Model):
    review = models.CharField(max_length=200)
    rating = models.FloatField('1 to 5')
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    
