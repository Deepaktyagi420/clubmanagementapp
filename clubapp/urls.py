from django.urls import path

from . import views

urlpatterns = [

    path('login/', views.UserLoginView.as_view(), name='login_page'),
    path('logout/', views.LogoutView.as_view(), name='logout_page'),
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('user-details/', views.UpdateUserDetailsView.as_view(), name='user_details'),
    path('booking-details/<int:pk>', views.BookingDetailView.as_view(), name='booking_details'),
    path('', views.HomeView.as_view(), name="home_page"),
    path('about-us/', views.AboutUsView.as_view(), name="about_us"),
    path('activity-list/', views.ActivitiesListView.as_view(), name="activity_list"),
    path('activity/<int:pk>', views.ActivityDetailView.as_view(), name="activity_detail"),
    path('my-booking/', views.MyBookingsView.as_view(), name="my_booking_view"),
]