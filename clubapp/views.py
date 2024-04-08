from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.views import View
from django.urls import reverse
from django.contrib.auth.models import User
from clubapp.models import ActivitiesModel, BookedActivity
from django.contrib.auth import logout

# Create your views here.
from datetime import datetime

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login_page")


class UpdateUserDetailsView(View):
    def get(self, request, *args, **kwargs):
        user_obj = User.objects.get(id=request.user.id)
        return render(
            request, template_name="user_details.html", context={"user_obj": user_obj}
        )

    def post(self, request, *args, **kwargs):
        request_dict = {}
        if (
            not request.POST.get("username")
            or not request.POST.get("name")
            or not request.POST.get("email")
            or not request.POST.get("password")
        ):
            user_obj = User.objects.get(id=request.user.id)
            return render(
                request,
                template_name="user_details.html",
                context={"error": "fields cannot be empty", "user_obj": user_obj},
            )
        user_obj = User.objects.get(id=request.user.id)
        user_obj.username = request.POST.get("username")
        user_obj.first_name = request.POST.get("name")
        user_obj.email = request.POST.get("email")
        user_obj.password = request.POST.get("password")
        try:
            user_obj.save()
        except IntegrityError as e:
            user_obj = User.objects.get(id=request.user.id)
            return render(
                request,
                template_name="user_details.html",
                context={"error": "username or email already", "user_obj": user_obj},
            )
        return redirect("user_details")


class UserLoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name="login.html", context={})

    def post(self, request, *args, **kwargs):
        username = request.POST["username"]
        password = request.POST["password_id"]
        user = User.objects.filter(username=username, password=password).first()
        if user:
            login(request, user)
            # Redirect to a success page.
            return redirect("home_page")
        else:
            # Return an 'invalid login' error message.
            return render(
                request,
                template_name="login.html",
                context={"error": "Invalid credentials"},
            )


class UserRegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name="register.html", context={})

    def post(self, request, *args, **kwargs):
        if request.POST.get("password") != request.POST.get("checkpassword"):
            return render(
                request,
                template_name="register.html",
                context={"error": "password does not match"},
            )

        if User.objects.filter(username=request.POST.get("username")).exists():
            return render(
                request,
                template_name="register.html",
                context={"error": "user already exists"},
            )

        if (
            not request.POST.get("name")
            or not request.POST.get("username")
            or not request.POST.get("email")
            or not request.POST.get("password")
        ):
            return render(
                request,
                template_name="register.html",
                context={"error": "Please fill all fields"},
            )

        fst_name = request.POST.get("name").split(" ")
        User.objects.create(
            username=request.POST.get("username"),
            email=request.POST.get("email"),
            first_name=fst_name,
            password=request.POST.get("password"),
        )

        return redirect("login_page")


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name="home.html", context={})


class AboutUsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name="aboutus.html", context={})


class ActivitiesListView(View):
    def get(self, request, *args, **kwargs):
        activity_lst = ActivitiesModel.objects.all()
        context = {"activity_list": activity_lst}
        return render(request, template_name="activities_lst.html", context=context)


class ActivityDetailView(View):
    error_msg = ""
    context = {}

    def get(self, request, pk, *args, **kwargs):
        activity_details = ActivitiesModel.objects.filter(id=pk).values().first()
        context = {"detail": activity_details}
        return render(request, template_name="activity_detail.html", context=context)

    def post(self, request, pk, *args, **kwargs):
        activity = ActivitiesModel.objects.filter(id=pk).first()
        try:
            date_of_booking = request.POST.get("date")
            date_of_booking = datetime.strptime(date_of_booking, "%Y-%m-%d")
            if date_of_booking <= datetime.now():
                activity_details = (
                    ActivitiesModel.objects.filter(id=pk).values().first()
                )
                context = {"detail": activity_details}
                context.update({"error": "Invalid date"})
                return render(
                    request, template_name="activity_detail.html", context=context
                )

            BookedActivity.objects.create(
                user=request.user,
                activity=activity,
                activity_slot=request.POST.get("time_frame"),
                date_of_booking=request.POST.get("date"),
            )
        except Exception as e:
            tt = "TT"
        url = reverse("my_booking_view")
        return redirect(url)


class MyBookingsView(View):
    def get(self, request, pk=None, *args, **kwargs):
        activties = BookedActivity.objects.filter(user=request.user)
        return render(
            request, template_name="mybookings.html", context={"booking_lst": activties}
        )
    
    
class BookingDetailView(View):
    error_msg = ""
    context = {}

    def get(self, request, pk, *args, **kwargs):
        booking_obj = BookedActivity.objects.filter(id=pk, user=request.user).first()
        if not booking_obj:
            return redirect("logout_page")
        context = {"detail": booking_obj}
        return render(request, template_name="booking_details.html", context=context)
    
    def post(self, request, pk=None, *args, **kwargs):

        BookedActivity.objects.filter(id=pk).delete()
        return redirect("my_booking_view")
