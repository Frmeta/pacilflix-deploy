from django.shortcuts import render

def tayangan_guest(request):
    return render(request, 'tayangan_guest.html')

def hasil_pencarian_guest(request):
    return render(request, 'hasil_pencarian_guest.html')

def tayangan_aktif(request):
    return render(request, 'tayangan_aktif.html')

def hasil_pencarian_aktif(request):
    return render(request, 'hasil_pencarian_aktif.html')

def hal_film_page(request):
    return render(request, 'hal_film.html')

def hal_series_page(request):
    return render(request, 'hal_series.html')

def hal_episode_page(request):
    return render(request, 'hal_episode.html')

def ulasan_page(request):
    return render(request, 'ulasan.html')




# fredo
def daftar_unduhan(request):
    return render(request, 'daftar_unduhan.html')

def daftar_favorit(request):
    context = {
        "data" : range(3)
    }
    return render(request, 'daftar_favorit.html', context)