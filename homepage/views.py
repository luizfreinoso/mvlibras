from django.shortcuts import render
from AP.models import AP
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required
def painel(request):
    aps = AP.objects.all().filter(publicado=True)
    rows = aps.count()/3
    return render(request, 'painel.html', {'aps': aps, 'rows': rows})