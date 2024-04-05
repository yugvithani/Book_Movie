from django.contrib import admin
from .models import RazorPayment, Theater, Movie, Show, Seat, Ticket

# Register your models here.

admin.site.register(Theater)
admin.site.register(Movie)
admin.site.register(Show)
admin.site.register(Seat)
admin.site.register(Ticket)
admin.site.register(RazorPayment)