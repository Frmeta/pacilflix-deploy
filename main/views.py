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
    context = {}
    with connection.cursor() as cursor:
        cursor.execute("SELECT judul, timestamp FROM tayangan_terunduh JOIN tayangan ON id_tayangan=id WHERE username = %s;", ["max_the_awesome"])
        rows = cursor.fetchall()
        print(rows)
        context = {'rows' : rows}

    return render(request, "daftar_unduhan.html", context)


def daftar_favorit(request):
    context = {}
    with connection.cursor() as cursor:
        cursor.execute("""
            select df.judul, df.timestamp, ARRAY_AGG(t.judul) as tayangan_list, ARRAY_AGG(tmdf.timestamp) as tayangan_timestamp_list
            from tayangan t join tayangan_memiliki_daftar_favorit as tmdf on t.id=tmdf.id_tayangan
            join daftar_favorit as df on tmdf.username=df.username and tmdf.timestamp=tmdf.timestamp
            group by (df.username, df.timestamp)
            having df.username=%s;""", ["max_the_awesome"])
        rows = cursor.fetchall()
        print(rows)

        daftar_daftar_favorit = []
        for row in rows:
            part1 = row[0]
            part2 = row[1]
            part3 = []
            for i in range(len(row[2])):
                part3.append((row[2][i], row[3][i]))
            daftar_favorit = (part1, part2, part3)
            daftar_daftar_favorit.append(daftar_favorit)
            print(daftar_favorit)
            
        context = {'daftar_daftar_favorit' : daftar_daftar_favorit}
    return render(request, "daftar_favorit.html", context)


# sabina
def kontributor(request):
    return render(request, 'kontributor.html')

def kontributor_pemain(request):
    return render(request, 'kontributor_pemain.html')

def kontributor_sutradara(request):
    return render(request, 'kontributor_sutradara.html')

def kontributor_penulis_skenario(request):
    return render(request, 'kontributor_penulis_skenario.html')

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
