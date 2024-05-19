from django.db import connection, DatabaseError
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
import uuid;
from django.utils import timezone
from django.core import serializers
from datetime import datetime, timedelta
import json

def tayangan_guest(request):
    # asumsi menampilkan 10 film dan 10 series
    with connection.cursor() as cursor:
        # GLOBAL
        # TOP 10 TAYANGAN
        cursor.execute("""
            SELECT 
                t.judul, 
                t.sinopsis, 
                t.url_video_trailer, 
                t.release_date_trailer, 
                COUNT(rn.username) AS total_views
            FROM 
                RIWAYAT_NONTON rn
            JOIN 
                TAYANGAN t ON rn.id_tayangan = t.id
            WHERE 
                rn.start_date_time >= NOW() - INTERVAL '7 days'
            GROUP BY 
                rn.id_tayangan, 
                t.judul, 
                t.sinopsis, 
                t.url_video_trailer, 
                t.release_date_trailer
            ORDER BY 
                total_views DESC
            LIMIT 10;
        """)
        data = cursor.fetchall()
        list_tayangan_global = []
        rank = 0
        for row in data:
            rank += 1
            hrefurl = row[2].split("=")[1]
            list_tayangan_global.append({
                'rank' : rank,
                'title' : row[0],
                'sinopsis' : row[1],
                'hrefurl' : hrefurl,
                'release_date' : row[3],
                'total_views' : row[4],
            })

        # TOP 10 FILM
        cursor.execute("""
            SELECT
                t.judul,
                t.sinopsis_trailer,
                t.url_video_trailer,
                t.release_date_trailer
            FROM
                FILM f
            JOIN
                TAYANGAN t ON f.id_tayangan = t.id
        """)
        data = cursor.fetchall()
        list_film_global = []
        for row in data:
            hrefurl = row[2].split("=")[1]
            list_film_global.append({
                'title' : row[0],
                'sinopsis' : row[1],
                'hrefurl' : hrefurl,
                'release_date' : row[3],
            })

        # TOP 10 SERIES
        cursor.execute("""
        SELECT
            t.judul,
            t.sinopsis_trailer,
            t.url_video_trailer,
            t.release_date_trailer
        FROM
            SERIES s
        JOIN
            TAYANGAN t ON s.id_tayangan = t.id
        """)
        data = cursor.fetchall()
        list_series_global = []  
        for row in data:
            hrefurl = row[2].split("=")[1]
            list_series_global.append({
                'title' : row[0],
                'sinopsis' : row[1],
                'hrefurl' : hrefurl,
                'release_date' : row[3],
            })

        # RETURN SEMUA DATA
        return render(request, "tayangan_guest.html", {
            'daftar1': list_tayangan_global,
            'daftar2': list_film_global,
            'daftar3': list_series_global
        })

def hasil_pencarian_guest(request):
    with connection.cursor() as cursor:
        if request.method == 'POST':
            search_text = request.POST.get('search', '')
            cursor.execute("""
                SELECT
                    t.judul,
                    t.sinopsis_trailer,
                    t.url_video_trailer,
                    t.release_date_trailer
                FROM
                    TAYANGAN t
                WHERE
                    t.judul ILIKE %s
            """, [f"%{search_text}%"])
            data = cursor.fetchall()
            list_hasil_pencarian = []  
            for row in data:
                hrefurl = row[2].split("=")[1]
                list_hasil_pencarian.append({
                    'title' : row[0],
                    'sinopsis' : row[1],
                    'hrefurl' : hrefurl,
                    'release_date' : row[3],
                })

            return render(request, "hasil_pencarian_guest.html", {
                'daftar': list_hasil_pencarian,
            })
        else:
            return render(request, "hasil_pencarian_guest.html")

def tayangan_aktif(request):
    username = request.COOKIES.get('username', '')
    if username == '':
        return redirect('/login/')
    with connection.cursor() as cursor:
        # TOP 10 TAYANGAN GLOBAL
        cursor.execute("""
            SELECT
                t.judul,
                t.sinopsis_trailer,
                t.url_video_trailer,
                t.release_date_trailer,
                COUNT(rn.username) AS total_views,
                t.id
            FROM 
                RIWAYAT_NONTON rn
            JOIN 
                TAYANGAN t ON rn.id_tayangan = t.id
            WHERE 
                rn.start_date_time >= NOW() - INTERVAL '7 days'
            GROUP BY 
                rn.id_tayangan, 
                t.judul, 
                t.sinopsis_trailer, 
                t.url_video_trailer, 
                t.release_date_trailer,
                t.id
            ORDER BY 
                total_views DESC
            LIMIT 10;
        """)
        data = cursor.fetchall()
        list_tayangan_global = []
        rank = 0
        for row in data:
            rank += 1
            hrefurl = row[2].split("=")[1]
            list_tayangan_global.append({
                'rank' : rank,
                'title' : row[0],
                'sinopsis' : row[1],
                'hrefurl' : hrefurl,
                'release_date' : row[3],
                'total_views' : row[4],
                'id' : row[5]
            })

        # TOP 10 FILM
        cursor.execute("""
            SELECT
                t.judul,
                t.sinopsis_trailer,
                t.url_video_trailer,
                t.release_date_trailer,
                t.id
            FROM
                FILM f
            JOIN
                TAYANGAN t ON f.id_tayangan = t.id
        """)
        data = cursor.fetchall()
        list_film_global = []
        for row in data:
            hrefurl = row[2].split("=")[1]
            list_film_global.append({
                'title' : row[0],
                'sinopsis' : row[1],
                'hrefurl' : hrefurl,
                'release_date' : row[3],
                'id' : row[4]
            })

        # TOP 10 SERIES
        cursor.execute("""
        SELECT
            t.judul,
            t.sinopsis_trailer,
            t.url_video_trailer,
            t.release_date_trailer,
            t.id
        FROM
            SERIES s
        JOIN
            TAYANGAN t ON s.id_tayangan = t.id
        """)
        data = cursor.fetchall()
        list_series_global = []  
        for row in data:
            hrefurl = row[2].split("=")[1]
            list_series_global.append({
                'title' : row[0],
                'sinopsis' : row[1],
                'hrefurl' : hrefurl,
                'release_date' : row[3],
                'id' : row[4]
            })
        
        paket_aktif = False
        cursor.execute("""
            SELECT COUNT(*)
            FROM TRANSACTION
            WHERE username = %s
            AND end_date_time > NOW()
        """, [username])
        result = cursor.fetchone()
        if result[0] > 0:
            paket_aktif = True

        # RETURN SEMUA DATA
        return render(request, "tayangan_aktif.html", {
            'daftar1': list_tayangan_global,
            'daftar2': list_film_global,
            'daftar3': list_series_global,
            'paket_aktif' : paket_aktif
        })

def hasil_pencarian_aktif(request):
    username = request.COOKIES.get('username', '')
    if username == '':
        return redirect('/login/')
    with connection.cursor() as cursor:
        if request.method == 'POST':
            search_text = request.POST.get('search', '')
            cursor.execute("""
                SELECT
                    t.judul,
                    t.sinopsis_trailer,
                    t.url_video_trailer,
                    t.release_date_trailer,
                    t.id
                FROM
                    TAYANGAN t
                WHERE
                    t.judul ILIKE %s
            """, [f"%{search_text}%"])
            data = cursor.fetchall()
            list_hasil_pencarian = []  
            for row in data:
                hrefurl = row[2].split("=")[1]
                list_hasil_pencarian.append({
                    'title' : row[0],
                    'sinopsis' : row[1],
                    'hrefurl' : hrefurl,
                    'release_date' : row[3],
                    'id' : row[4]
                })
            
            paket_aktif = False
            cursor.execute("""
                SELECT COUNT(*)
                FROM TRANSACTION
                WHERE username = %s
                AND end_date_time > NOW()
            """, [username])
            result = cursor.fetchone()
            if result[0] > 0:
                paket_aktif = True

            return render(request, "hasil_pencarian_aktif.html", {
                'daftar': list_hasil_pencarian,
                'paket_aktif' : paket_aktif
            })
        else:
            return render(request, "hasil_pencarian_aktif.html")

def detail_page(request, id):
    username = request.COOKIES.get('username', '')
    if username == '':
        return redirect('/login/')
    is_film = False
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT *
            FROM film
            WHERE id_tayangan = %s
        """, [id])
        if cursor.rowcount > 0:
            is_film = True
    # JIKA TAYANGAN ADALAH FILM
    if is_film:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    t.judul,
                    (
                        SELECT COUNT(*)
                        FROM RIWAYAT_NONTON rn
                        WHERE rn.id_tayangan = t.id
                    ) AS total_view,
                    (
                        SELECT AVG(u.rating)
                        FROM ULASAN u
                        WHERE u.id_tayangan = t.id
                    ) AS avg_rating,
                    t.sinopsis,
                    f.durasi_film,
                    f.release_date_film,
                    f.url_video_film,
                    (
                        SELECT STRING_AGG(g.genre,', ')
                        FROM GENRE_TAYANGAN g
                        WHERE g.id_tayangan = t.id
                    ) AS genre,
                    t.asal_negara,
                    (
                        SELECT STRING_AGG(c.nama, ', ')
                        FROM CONTRIBUTORS c
                        JOIN PEMAIN p ON c.id = p.id
                        JOIN MEMAINKAN_TAYANGAN mt ON p.id = mt.id_pemain
                        WHERE mt.id_tayangan = t.id
                    ) AS pemain,
                    (
                        SELECT STRING_AGG(c.nama, ', ')
                        FROM CONTRIBUTORS c
                        JOIN PENULIS_SKENARIO ps ON c.id = ps.id
                        JOIN MENULIS_SKENARIO_TAYANGAN mst ON ps.id = mst.id_penulis_skenario
                        WHERE mst.id_tayangan = t.id
                    ) AS penulis_skenario,
                    (
                        SELECT c.nama
                        FROM CONTRIBUTORS c
                        JOIN SUTRADARA s ON c.id = s.id
                        JOIN TAYANGAN t2 ON s.id = t2.id_sutradara
                        WHERE t2.id = t.id
                    ) AS sutradara
                FROM
                    TAYANGAN t
                JOIN
                    FILM f ON t.id = f.id_tayangan
                WHERE
                    t.id = %s
                LIMIT 1;
            """, [id])
            data = cursor.fetchall()
            list_hasil_pencarian = []  
            genre_list = []
            pemain_list = []
            penulis_skenario_list = []
            for row in data:
                if row[7] is not None:
                    genre_list = row[7].split(", ")
                if row[9] is not None:
                    pemain_list = row[9].split(", ")
                if row[10] is not None:
                    penulis_skenario_list = row[10].split(", ")
                if row[6] != "unreleased":
                    url_video = row[6].split("=")[1]
                else:
                    url_video = row[6]
                avg_rating = 0.0
                if row[2] is not None:
                    avg_rating = "%.1f" % row[2]
                list_hasil_pencarian.append({
                    'title' : row[0],
                    'total_view' : row[1],
                    'avg_rating' : avg_rating,
                    'sinopsis' : row[3],
                    'durasi_film' : row[4],
                    'release_date_film' : row[5],
                    'url_video_film' : url_video,
                    'asal_negara' : row[8],
                    'sutradara' : row[11],
                    'id' : id
                })

            # fetch ulasan
            cursor.execute("""
                SELECT
                    u.username,
                    u.rating,
                    u.deskripsi,
                    u.timestamp
                FROM
                    ULASAN u
                JOIN
                    TAYANGAN t ON u.id_tayangan = t.id
                WHERE
                    t.id = %s
                ORDER BY
                    u.timestamp DESC
            """, [id])
            data = cursor.fetchall()
            list_ulasan = []
            for row in data:
                avg_rating = 0.0
                if row[1] is not None:
                    avg_rating = "%.1f" % row[1]
                list_ulasan.append({
                    'username' : row[0],
                    'rating' : avg_rating,
                    'deskripsi' : row[2],
                    'timestamp' : row[3],
                })

            return render(request, "film.html", {
                'daftar': list_hasil_pencarian,
                'daftar2' : list_ulasan,
                'pemain_list' : pemain_list,
                'penulis_skenario_list' : penulis_skenario_list,
                'genre_list' : genre_list,
                'id' : id
            })
    else: # JIKA TAYANGAN ADALAH SERIES
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    t.judul,
                    (
                        SELECT COUNT(*)
                        FROM RIWAYAT_NONTON rn
                        WHERE rn.id_tayangan = t.id
                    ) AS total_view,
                    (
                        SELECT AVG(u.rating)
                        FROM ULASAN u
                        WHERE u.id_tayangan = t.id
                    ) AS avg_rating,
                    t.sinopsis,
                    (
                        SELECT STRING_AGG(g.genre, ', ')
                        FROM GENRE_TAYANGAN g
                        WHERE g.id_tayangan = t.id
                    ) AS genre_list,
                    t.asal_negara,
                    (
                        SELECT STRING_AGG(p.nama, ', ')
                        FROM CONTRIBUTORS p
                        JOIN PEMAIN pm ON p.id = pm.id
                        JOIN MEMAINKAN_TAYANGAN mt ON pm.id = mt.id_pemain
                        WHERE mt.id_tayangan = t.id
                    ) AS pemain_list,
                    (
                        SELECT STRING_AGG(ps.nama, ', ')
                        FROM CONTRIBUTORS ps
                        JOIN PENULIS_SKENARIO psk ON ps.id = psk.id
                        JOIN MENULIS_SKENARIO_TAYANGAN mst ON psk.id = mst.id_penulis_skenario
                        WHERE mst.id_tayangan = t.id
                    ) AS penulis_skenario_list,
                    (
                        SELECT c.nama
                        FROM CONTRIBUTORS c
                        JOIN SUTRADARA s ON c.id = s.id
                        JOIN TAYANGAN t2 ON s.id = t2.id_sutradara
                        WHERE t2.id = t.id
                    ) AS sutradara,
                    (
                        SELECT STRING_AGG(DISTINCT e.sub_judul, ', ')
                        FROM SERIES s
                        JOIN EPISODE e ON s.id_tayangan = e.id_series
                        WHERE s.id_tayangan = t.id
                    ) AS episodes
                FROM
                    TAYANGAN t
                JOIN
                    SERIES s ON t.id = s.id_tayangan
                WHERE
                    t.id = %s
                LIMIT 1;
            """, [id])
            data = cursor.fetchall()
            list_hasil_pencarian = []
            for row in data:
                avg_rating = 0.0
                genre_list = []
                pemain_list = []
                penulis_skenario_list = []
                episode_list = []
                if row[2] is not None:
                    avg_rating = "%.1f" % row[2]
                if row[4] is not None:
                    genre_list = row[4].split(", ")
                if row[6] is not None:
                    pemain_list = row[6].split(", ")
                if row[7] is not None:
                    penulis_skenario_list = row[7].split(", ")
                if row[9] is not None:
                    episode_list = row[9].split(", ")
                list_hasil_pencarian.append({
                    'title' : row[0],
                    'total_view' : row[1],
                    'avg_rating' : avg_rating,
                    'sinopsis' : row[3],
                    'asal_negara' : row[5],
                    'sutradara' : row[8]
                })

             # fetch ulasan
            cursor.execute("""
                SELECT
                    u.username,
                    u.rating,
                    u.deskripsi,
                    u.timestamp
                FROM
                    ULASAN u
                JOIN
                    TAYANGAN t ON u.id_tayangan = t.id
                WHERE
                    t.id = %s
                ORDER BY
                    u.timestamp DESC
            """, [id])
            data = cursor.fetchall()
            list_ulasan = []
            for row in data:
                avg_rating = 0.0
                if row[1] is not None:
                    avg_rating = "%.1f" % row[1]
                list_ulasan.append({
                    'username' : row[0],
                    'rating' : avg_rating,
                    'deskripsi' : row[2],
                    'timestamp' : row[3],
                })

            return render(request, "series.html", {
                'daftar': list_hasil_pencarian,
                'daftar2' : list_ulasan,
                'pemain_list': pemain_list,
                'penulis_skenario_list' : penulis_skenario_list,
                'genre_list' : genre_list,
                'episode_list' : episode_list,
                'id' : id
            })
        
def episode_page(request, title, id):
    username = request.COOKIES.get('username', '')
    if username == '':
        return redirect('/login/')
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                t.judul,
                e.sub_judul,
                e.sinopsis,
                e.durasi,
                e.url_video,
                e.release_date,
                (
                    SELECT STRING_AGG(DISTINCT e.sub_judul, ', ')
                    FROM SERIES s
                    JOIN EPISODE e ON s.id_tayangan = e.id_series
                    WHERE s.id_tayangan = t.id
                ) AS episodes
            FROM
                EPISODE e
            JOIN
                SERIES s ON s.id_tayangan = e.id_series
            JOIN
                TAYANGAN t ON t.id = s.id_tayangan
            WHERE
                e.sub_judul = %s
            AND
                e.id_series = %s
        """, [title, id])
        data = cursor.fetchall()
    episode_list = []
    for row in data:
        if row[6] is not None:
            episodes = row[6].split(", ")
        if row[4] != "unreleased":
            url_video = row[4].split("=")[1]
        else:
            url_video = row[4]
        episode_list.append({
            'title': row[0],
            'sub_judul': row[1],
            'sinopsis': row[2],
            'durasi': row[3],
            'url': url_video,
            'release_date': row[5],
            'id' : id
        })

    episodes.remove(title)
    context = {
        'daftar': episode_list,
        'episode_list' : episodes,
        'id' : id
    }
    return render(request, 'episode.html', context)

def watch(request, id):
    ''' ASUMSI
    jika pengguna mensubmit watch dengan progress >= 70% maka akan disimpan ke riwayat_nonton
    sedangkan jika < 70% maka tidak akan disimpan
    sehingga views yang ditampilkan (yang diambil dari riwayat_nonton) dipastikan >= 70%
    ''' 
    username = request.COOKIES.get('username', '')
    if username == '':
        return redirect('/login/')
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO RIWAYAT_NONTON (id_tayangan, username, start_date_time, end_date_time)
                VALUES (%s, %s, NOW(), NOW())
            """, [id, username])
        return JsonResponse({'status': 'success'})

def review(request, id):
    username = request.COOKIES.get('username', '')
    if username == '':
        return redirect('/login/')
    if request.method == 'POST':
        with connection.cursor() as cursor:
            data = json.loads(request.body)
            id = data.get('id')
            rating = int(data.get('rating'))
            deskripsi = data.get('deskripsi')
            cursor.execute("""
                INSERT INTO ULASAN (id_tayangan, username, timestamp, rating, deskripsi)
                VALUES (%s, %s, NOW(), %s, %s)
            """, [id, username, rating, deskripsi])
            return JsonResponse({'status': 'success'})

# fredo
#@login_required
def daftar_unduhan(request):
    username = request.COOKIES.get('username')
    if username is None:
        return HttpResponseBadRequest("Missing 'username' parameter in cookies.")
    
    context = {}
    with connection.cursor() as cursor:
        cursor.execute("SELECT judul, timestamp, id FROM tayangan_terunduh JOIN tayangan ON id_tayangan=id WHERE username = %s;", [username])
        connection.commit()
        rows = cursor.fetchall()
        
        output = []
        for row in rows:
            output.append((row[0], row[1].strftime("%Y-%m-%d %H:%M:%S.%f"), row[2]))

        context = {'rows' : output}

    return render(request, "daftar_unduhan.html", context)


#@login_required
def unduh(request):
    if request.method == 'POST':
        tayangan_id = request.POST.get('id')
        username = request.COOKIES.get("username")
        if not username:
            return HttpResponseBadRequest("Missing 'username' parameter in cookies.")

        if not tayangan_id:
            return HttpResponseBadRequest("Missing 'id' parameter in request body.")
        try:
            uuid.UUID(tayangan_id)
        except ValueError:
            return HttpResponseBadRequest("Invalid format for 'id'. Expected UUID.")
        
        with connection.cursor() as cursor:
            now = datetime.now()
            rows_affected = cursor.execute("insert into tayangan_terunduh values (%s, %s, %s);", [tayangan_id, username, datetime.now()])
            connection.commit()
            return JsonResponse({'valid_till' : (now + timedelta(hours=24)).isoformat()})

    return HttpResponseBadRequest("Bad Request")

def hapus_unduhan(request):
    if request.method == 'POST':
        tayangan_id = request.POST.get('id')
        timestamp = request.POST.get('timestamp')
        username = request.COOKIES.get("username")
        if not username: return HttpResponseBadRequest("Missing 'username' parameter in cookies.")
        if not tayangan_id: return HttpResponseBadRequest("Missing 'id' parameter in request body.")

        try:
            uuid.UUID(tayangan_id)
        except ValueError:
            return HttpResponseBadRequest("Invalid format for 'id'. Expected UUID.")

        with connection.cursor() as cursor:
            try:
                cursor.execute("delete from tayangan_terunduh where id_tayangan=%s and username=%s and timestamp=%s;", [tayangan_id, username, timestamp])
                connection.commit()
            except Exception as e:
                return JsonResponse({'status': 'failed', 'message': str(e)})
            
            return JsonResponse({'status': 'success'})

    return HttpResponseBadRequest("Bad Request")



#@login_required
def daftar_favorit(request):
    return render(request, "daftar_favorit.html")

def bikin_daftar_favorit(request):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        username = request.COOKIES.get("username")
        if not username: return HttpResponseBadRequest("Missing 'username' parameter in cookies.")
        if not judul: return HttpResponseBadRequest("Missing 'id' parameter in request body.")
    
        context = {}
        with connection.cursor() as cursor:
            try:
                cursor.execute("""
                    insert into daftar_favorit (timestamp, username, judul) values (NOW(), %s, %s);""", [username, judul])
                connection.commit()
            except Exception as e:
                return redirect('daftar_favorit')

            return redirect('daftar_favorit')
                                
    return HttpResponseBadRequest("Bad Request")

def get_daftar_favorit(request):
    username = request.COOKIES.get("username")
    if not username: return HttpResponseBadRequest("Missing 'username' parameter in cookies.")

    with connection.cursor() as cursor:
        cursor.execute("select timestamp, username, judul from daftar_favorit where username=%s;", [username])
        connection.commit()
        rows = cursor.fetchall()
        
        output = []
        for row in rows:
            output.append({'timestamp':row[0].strftime("%Y-%m-%d %H:%M:%S.%f"), 'username':row[1], 'judul':row[2]})
        return JsonResponse(output, safe=False)

def delete_daftar_favorit(request):
    if request.method == 'POST':
        username = request.COOKIES.get("username")
        if not username: return HttpResponseBadRequest("Missing 'username' parameter in cookies.")
        timestamp = request.POST.get("timestamp")
        

        with connection.cursor() as cursor:
            try:
                cursor.execute("delete from daftar_favorit where timestamp=%s and username=%s;", [timestamp, username])
                connection.commit()
            except Exception as e:
                return HttpResponseBadRequest("NOT OK")

            return JsonResponse({'status' : 'success'})


    # If the request method is not POST, redirect to some view
    return HttpResponseBadRequest("Bad Request")

def tambah_favorit(request):
    if request.method == 'POST':
        username = request.COOKIES.get("username")
        if not username: return HttpResponseBadRequest("Missing 'username' parameter in cookies.")

        favorit = request.POST.get('favorit')
        favorit = favorit.split('woi')
        print(favorit)
        
        timestamp = favorit[0]
        id_tayangan = favorit[1]

        with connection.cursor() as cursor:
            try:
                cursor.execute("insert into tayangan_memiliki_daftar_favorit (id_tayangan, timestamp, username) values (%s, %s, %s);", [id_tayangan, timestamp, username])
                connection.commit()
            except Exception as e:
                return JsonResponse({'status' : 'failed', 'message' : str(e)})

            return JsonResponse({'status' : 'success'})


    # If the request method is not POST, redirect to some view
    return HttpResponseBadRequest("Bad Request")

def detail_daftar_favorit(request, timestamp):
    username = request.COOKIES.get("username")
    if not username: return HttpResponseBadRequest("Missing 'username' parameter in cookies.")

    with connection.cursor() as cursor:
        cursor.execute("SELECT judul from daftar_favorit where username=%s AND timestamp=%s", [username, timestamp])
        connection.commit()
        rows = cursor.fetchall()

    context = {"timestamp" : timestamp, "judul" : rows[0][0]}
    return render(request, "detail_daftar_favorit.html", context)

def get_detail_daftar_favorit(request):
    username = request.COOKIES.get("username")
    if not username: return HttpResponseBadRequest("Missing 'username' parameter in cookies.")

    timestamp = request.GET.get("timestamp")

    with connection.cursor() as cursor:
        cursor.execute("""SELECT df.timestamp, df.username, t.judul, t.id
                        FROM tayangan_memiliki_daftar_favorit tmdf
                        JOIN daftar_favorit df ON tmdf.username=df.username and tmdf.timestamp=df.timestamp 
                        JOIN tayangan t on t.id=id_tayangan
                        WHERE df.username=%s and df.timestamp=%s;""", [username, timestamp])
        connection.commit()
        rows = cursor.fetchall()
        
        output = []
        for row in rows:
            output.append(
                {'timestamp':row[0].strftime("%Y-%m-%d %H:%M:%S.%f"),
                 'username':row[1],
                 'judul':row[2],
                 'id_tayangan':row[3]})
        return JsonResponse(output, safe=False)
    
def delete_tayangan_di_daftar_favorit(request):
    username = request.COOKIES.get("username")
    timestamp = request.POST.get("timestamp")
    id_tayangan = request.POST.get("id_tayangan")

    if request.method != 'POST' or not timestamp or not id_tayangan or not username:
        return HttpResponseBadRequest("Bad Request!")
    
    with connection.cursor() as cursor:
        cursor.execute("""
                        DELETE FROM TAYANGAN_MEMILIKI_DAFTAR_FAVORIT
                        WHERE USERNAME=%s AND TIMESTAMP=%s AND ID_TAYANGAN=%s;
                       """, [username, timestamp, id_tayangan])
        connection.commit()
        return HttpResponse("OK")

# sabina
def kontributor(request):
    return render(request, "kontributor.html")


def kontributor_pemain(request):
    return render(request, "kontributor_pemain.html")


def kontributor_sutradara(request):
    return render(request, "kontributor_sutradara.html")


def kontributor_penulis_skenario(request):
    return render(request, "kontributor_penulis_skenario.html")


def langganan(request):
    return render(request, "langganan.html")


def update_langganan(request):
    return render(request, "update_langganan.html")


def main(request):
    return render(request, "main.html")