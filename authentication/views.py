from django.db import connection
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


class LoggedInUser:
    username = ""


def register_page(request):
    return render(request, "register.html")


@csrf_exempt
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        negara = request.POST.get("negara")
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO pengguna (username, password, asal_negara)
                VALUES (%s, %s, %s)
            """,
                (username, password, negara),
            )
            return redirect("login")
        except Exception as e:
            error_message = str(e)
            if "username" in error_message:
                error_message = "Username sudah terdaftar!"
            return render(request, "register.html", {"error_message": error_message})
    return render(request, "register.html")


@csrf_exempt
def login(request):
    context = {"error": ""}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    f"SELECT username, asal_negara FROM pengguna WHERE username='{username}' AND password='{password}';"
                )
                result = cursor.fetchall()
            except Exception as e:
                context["error"] = str(e)
                return render(request, "login.html", context)

        if len(result) != 0:
            username = result[0][0]
            negara = result[0][1]
            response = HttpResponseRedirect(reverse("tayangan"))
            response.set_cookie("username", username)
            response.set_cookie("negara", negara)
            response.set_cookie("is_authenticated", "True")
            return response
        else:
            context["error"] = "Username atau password salah! Silakan coba lagi."

    return render(request, "login.html", context)


def logout_user(request):
    response = HttpResponseRedirect(reverse("show_main"))
    response.delete_cookie("username")
    response.delete_cookie("negara")
    response.delete_cookie("is_authenticated")
    LoggedInUser.username = ""
    return response


def show_main(request):
    context = {}
    return render(request, "blankRegist.html", context)
