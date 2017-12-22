from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'apaeld.html')

def TradutorDatilologia(request):
    return render(request, 'TradutorDatilologia.html')