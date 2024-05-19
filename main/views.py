from django.db import connection
from django.shortcuts import render, redirect

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
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                t.username,
                p.nama,
                STRING_AGG(pr.dukungan_perangkat, ', ') AS perangkat,
                p.harga,
                p.resolusi_layar,
                t.start_date_time,
                t.end_date_time,
                t.metode_pembayaran,
                t.timestamp_pembayaran,
                CASE
                    WHEN CURRENT_DATE BETWEEN t.start_date_time AND t.end_date_time THEN 'current'
                    ELSE 'past'
                END AS status
            FROM
                transaction t
            JOIN 
                paket p ON t.nama_paket = p.nama
            JOIN 
                dukungan_perangkat pr ON p.nama = pr.nama_paket
            WHERE 
                t.username = %s
            GROUP BY 
                t.username, p.nama, p.harga, p.resolusi_layar, t.start_date_time, t.end_date_time, t.metode_pembayaran, t.timestamp_pembayaran
            ORDER BY 
                t.start_date_time DESC;
        """, ["jackAttack"])
        rows = cursor.fetchall()
        
        current_paket = {
            'nama': '-',
            'perangkat': '-',
            'harga': '-',
            'resolusi_layar': '-',
            'start_date_time': '-',
            'end_date_time': '-',
            'metode_pembayaran': '-',
            'timestamp_pembayaran': '-',
        }
        past_pakets = []
        
        for row in rows:
            paket = {
                'nama': row[1],
                'perangkat': row[2],
                'harga': row[3],
                'resolusi_layar': row[4],
                'start_date_time': row[5],
                'end_date_time': row[6],
                'metode_pembayaran': row[7],
                'timestamp_pembayaran': row[8],
            }
            if row[9] == 'current':
                current_paket = paket
            else:
                past_pakets.append(paket)
        
        context = {
            'username': 'jackAttack',
            'current_paket': current_paket,
            'past_pakets': past_pakets,
        }
    
    return render(request, 'langganan.html', context)

def update_langganan(request):
    context={}
    with connection.cursor() as cursor:
        cursor.execute("""SELECT 
                            p.nama,
                            p.harga,
                            p.resolusi_layar,
                            STRING_AGG(dp.dukungan_perangkat, ', ') AS perangkat
                        FROM 
                            paket p
                        JOIN 
                            dukungan_perangkat dp ON p.nama = dp.nama_paket
                        GROUP BY 
                            p.nama, p.harga, p.resolusi_layar;""")
        rows = cursor.fetchall()
        print(rows)
        context = {'rows': rows}

    if request.method == 'POST':
        username = 'jackAttack'
        nama_paket = request.POST['nama_paket']
        metode_pembayaran = request.POST['metode_pembayaran']

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO transaction (username, nama_paket, start_date_time, end_date_time, metode_pembayaran, timestamp_pembayaran)
                    VALUES (%s, %s, CURRENT_DATE, CURRENT_DATE + INTERVAL '1 month', %s, CURRENT_TIMESTAMP);
                """, [username, nama_paket, metode_pembayaran])

        return redirect('/langganan/')

    return render(request, 'update_langganan.html', context)

# ariana
def login(request):
    return render(request, "login.html")


def home(request):
    return render(request, "home.html")


def profile(request):
    return render(request, "profile.html")
