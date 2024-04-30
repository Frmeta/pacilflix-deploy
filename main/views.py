from django.shortcuts import render

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
