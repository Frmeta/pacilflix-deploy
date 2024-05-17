from django.db import connection
from django.shortcuts import render

def tayangan_guest(request):
    return render(request, "tayangan_guest.html")


def hasil_pencarian_guest(request):
    return render(request, "hasil_pencarian_guest.html")


def tayangan_aktif(request):
    return render(request, "tayangan_aktif.html")


def hasil_pencarian_aktif(request):
    return render(request, "hasil_pencarian_aktif.html")


def hal_film_page(request):
    return render(request, "hal_film.html")


def hal_series_page(request):
    return render(request, "hal_series.html")


def hal_episode_page(request):
    return render(request, "hal_episode.html")


def ulasan_page(request):
    return render(request, "ulasan.html")


# fredo
def daftar_unduhan(request):
    return render(request, "daftar_unduhan.html")


def daftar_favorit(request):
    context = {"data": range(3)}
    return render(request, "daftar_favorit.html", context)


# sabina
def kontributor(request):
    context = {}
    with connection.cursor() as cursor:
        cursor.execute("""SELECT 
                            c.id, c.nama,
                            CASE
                            WHEN c.jenis_kelamin = 0 THEN 'M'
                            WHEN c.jenis_kelamin = 1 THEN 'F'
                            END AS jenis_kelamin,
                            STRING_AGG(t.type, ', ') AS types,
                            c.kewarganegaraan
                        FROM (
                            (SELECT c.id, c.nama, c.jenis_kelamin, 'Pemain' AS type, c.kewarganegaraan
                            FROM contributors c
                            JOIN pemain w ON c.id = w.id)
                            UNION
                            (SELECT c.id, c.nama, c.jenis_kelamin, 'Sutradara' AS type, c.kewarganegaraan
                            FROM contributors c
                            JOIN sutradara d ON c.id = d.id)
                            UNION
                            (SELECT c.id, c.nama, c.jenis_kelamin, 'Penulis Skenario' AS type, c.kewarganegaraan
                            FROM contributors c
                            JOIN penulis_skenario ps ON c.id = ps.id)
                        ) t
                        JOIN contributors c ON t.id = c.id
                        GROUP BY c.id, c.nama
                        ORDER BY 
                            c.nama;""")
        rows = cursor.fetchall()
        print(rows)
        context = {'rows': rows}

    return render(request, 'kontributor.html', context)

def kontributor_pemain(request):
    context = {}
    with connection.cursor() as cursor:
        cursor.execute("""SELECT nama,
                        CASE
                        WHEN jenis_kelamin = 0 THEN 'M'
                        WHEN jenis_kelamin = 1 THEN 'F'
                        END AS jenis_kelamin,
                        kewarganegaraan
                        FROM contributors
                        NATURAL JOIN pemain;""")
        rows = cursor.fetchall()
        print(rows)
        context = {'rows': rows}

    return render(request, 'kontributor_pemain.html', context)

def kontributor_sutradara(request):
    context = {}
    with connection.cursor() as cursor:
        cursor.execute("""SELECT nama,
                        CASE
                        WHEN jenis_kelamin = 0 THEN 'M'
                        WHEN jenis_kelamin = 1 THEN 'F'
                        END AS jenis_kelamin,
                        kewarganegaraan
                        FROM contributors
                        NATURAL JOIN sutradara;""")
        rows = cursor.fetchall()
        print(rows)
        context = {'rows': rows}

    return render(request, 'kontributor_sutradara.html', context)

def kontributor_penulis_skenario(request):
    context = {}
    with connection.cursor() as cursor:
        cursor.execute("""SELECT nama,
                        CASE
                        WHEN jenis_kelamin = 0 THEN 'M'
                        WHEN jenis_kelamin = 1 THEN 'F'
                        END AS jenis_kelamin,
                        kewarganegaraan
                        FROM contributors
                        NATURAL JOIN penulis_skenario;""")
        rows = cursor.fetchall()
        print(rows)
        context = {'rows': rows}

    return render(request, 'kontributor_penulis_skenario.html', context)

def langganan(request):
    return render(request, 'langganan.html')

def update_langganan(request):
    return render(request, 'update_langganan.html')

# ariana
def login(request):
    return render(request, "login.html")


def home(request):
    return render(request, "home.html")


def profile(request):
    return render(request, "profile.html")
