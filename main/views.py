from django.shortcuts import render

def hal_film_page(request):
    return render(request, 'hal_film.html')

def hal_series_page(request):
    return render(request, 'hal_series.html')

def hal_episode_page(request):
    return render(request, 'hal_episode.html')

def ulasan_page(request):
    return render(request, 'ulasan.html')