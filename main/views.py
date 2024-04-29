from django.shortcuts import render

def kontributor(request):
    return render(request, 'kontributor.html')

def langganan(request):
    return render(request, 'langganan.html')

def update_langganan(request):
    return render(request, 'update_langganan.html')
