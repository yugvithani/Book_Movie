from django.urls import path
from . import views
app_name = "book_movie"

urlpatterns = [
    path("register/", views.register_user, name="register"),
    path("", views.login_user, name="login"),
    path("accounts/login/", views.login_user, name="login"),
    path("home/login/", views.login_user, name="login"),
    path("movie/login/", views.login_user, name="login"),
    path("home/", views.home, name="home"),
    path("home/logout/", views.logout_user, name="logout"),
    path("movie/logout/", views.logout_user, name="logout"),
    path("my_booking/", views.my_booking, name="my_booking"),
    path("full_ticket/<int:ticket_no>", views.full_ticket, name="full_ticket"),
    
    path("movie/", views.movie_list, name="movie_list"),
    path("movie_details/<int:movie_id>", views.movie_details, name="movie_details"),
    path("movie/add_movie/", views.add_movie, name="add_movie"),
    path("movie_details/update_movie/<int:id>", views.update_movie, name="update_movie"),
    path("movie_details/updated_movie/<int:id>", views.updated_movie, name="updated_movie"),
    path("movie_details/delete_movie/<int:id>", views.delete_movie, name="delete_movie"),
    path("movie_show/<int:movie_id>", views.movie_show, name="movie_show"),
    path("seat_map/<int:Show_id>", views.seat_map, name="seat_map"),
    # path("payment/", views.payment, name="payment"),
    path('payment/', views.payment_page, name='payment'),
    # path('movie/payment_success/', views.payment_success, name='payment_success'),
    path("payment/book_successfully/", views.book_successfully, name="book_successfully"),
    
    path("movie/theater_list/", views.theater_list_admin, name="theater_list_admin"),
    path('movie_details/<int:movie_id>/book/', views.book, name='book'),
    path("movie/<int:movie_id>/theater/", views.theater_list, name="theater_list"),
    path("movie/theater_list/<str:pk>", views.theater_details, name="theater_details"),

    path('movie/theater_list/update_Theater/<int:id>', views.update_Theater, name='update_Theater'),
    path('movie/theater_list_admin/updated_Theater/<int:id>', views.updated_Theater, name='updated_Theater'),
    path('movie/theater_list/delete_theater/<int:id>', views.delete_Theater, name='delete_Theater'),
    path('movie/theater_list/add_theater/', views.add_Theater, name='add_Theater'),
    
    path("movie/show_list/", views.show_list, name="show_list"),
    path("movie/show_list/<int:id>", views.show_details, name="show_details"),
    path("movie/show_list/update_show/<int:id>", views.update_show, name="update_show"),
    path("movie/show_list/updated_show/<int:id>", views.updated_show, name="updated_show"),
    path("movie/show_list/delete_show/<int:id>", views.delete_show, name="delete_show"),
    path("movie/show_list/add_show/", views.add_show, name="add_show"),
    
    path('movie/rating/', views.rating, name='rating'),
    path('movie/rating/add/', views.add_rating, name='add_rating'),
    # path('movie/rating/', views.rating, name="rating"),
    # accounts/login/
]   