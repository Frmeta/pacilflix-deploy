from django.shortcuts import render

def kontributor_page(request):
    return render(request, 'kontributor.html')

def langganan_page(request):
    return render(request, 'langganan.html')

def update_langganan_page(request):
    return render(request, 'update_langganan.html')