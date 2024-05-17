from django.db import connection
from django.shortcuts import render
import datetime
from django.http import HttpResponseRedirect

# from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.db.utils import IntegrityError


# Create your views here.
# ariana
# def login(request):
#     return render(request, "login.html")


# def home(request):
#     return render(request, "home.html")


def profile(request):
    return render(request, "profile.html")


@csrf_exempt
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        negara = request.POST.get("negara")
        messages = []

        if not username or not password1 or not negara:
            messages.append("All fields are required.")
        elif len(username) < 3 or len(password1) < 6:
            messages.append(
                "Username must be at least 3 characters and password must be at least 6 characters."
            )
        if len(negara) < 2:
            messages.append("Country must be at least 2 characters long.")
        if password1 != password2:
            messages.append("Password one and two must be same")

        if messages:
            return render(request, "home.html", {"messages": messages})

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    rf"""
                SET search_path to pacilflix;
                INSERT INTO pengguna VALUES ('{username}', '{password1}', '{negara}')"""
                )
        except Exception as e:
            messages.append(
                "Username dengan nama tersebut sudah ada, silahkan coba yang lain!"
            )
            return render(request, "register.html", {"messages": messages})
        return HttpResponseRedirect(reverse("authentication:login"))

    return render(request, "home.html")


@csrf_exempt
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        messages = []

        if not username or not password:
            messages.append("Username and password are required.")
        elif len(username) < 3 or len(password) < 6:
            messages.append(
                "Username must be at least 3 characters and password must be at least 6 characters."
            )

        if messages:
            return render(request, "login.html", {"messages": messages})

        with connection.cursor() as cursor:
            cursor.execute(
                rf"""
            SET search_path to pacilflix;
            SELECT * FROM pengguna WHERE username = '{username}' AND password = '{password}'
            """
            )
            user = cursor.fetchone()

        if user:
            with connection.cursor() as cursor:
                cursor.execute(
                    rf"""
                SET search_path to public;
                """
                )
            request.session["username"] = username
            response = HttpResponseRedirect(reverse("main:home"))
            response.set_cookie("username", username)
            response.set_cookie("negara_asal", user[2])
            response.set_cookie("last_login", str(datetime.datetime.now()))
            return response
        else:
            messages.append("Sorry, incorrect username or password. Please try again.")
            return render(request, "login.html", {"messages": messages})

    return render(request, "login.html")


@csrf_exempt
def logout(request):
    with connection.cursor() as cursor:
        cursor.execute(
            rf"""
                SET search_path to public;
                """
        )
    response = HttpResponseRedirect(reverse("main:home"))
    request.session.flush()
    response.delete_cookie("last_login")
    response.delete_cookie("username")
    response.delete_cookie("negara_asal")
    return response
