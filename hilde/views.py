from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from datetime import datetime
from chartit import DataPool, Chart
from models import Walter

# Create your views here.

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def tagesfarbe():
    zeit = datetime.now()
    r = zeit.second*3
    g = 100+zeit.minute*2
    b = zeit.hour*5
    rgb = r,g,b
    return rgb


def index(request):
    Grafik = DataPool(
        series=
        [{'options': {
            'source': Walter.objects.all()},
            'terms':[
                'x',
                'y']}
            ])
    chart = Chart(
        datasource = Grafik,
        series_options =
            [{'options':{
                'type': 'line',
                'stacking': False},
                'terms':{
                  'x':['y']
                }}],
        chart_options =
            {'title': {
                   'text': 'Testgrafik'},
               })

    return render(request,'hilde/index.html',{'farbe':rgb_to_hex(tagesfarbe()),'chart':chart})
    
def einloggen(request):
    username = request.POST['username']
    passwort = request.POST['password']
    user = authenticate(username=username, password=passwort)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/admin/')
        return HttpResponse('Fehler - Account inaktiv')
    return HttpResponse('Fehler - falscher Username oder falsches Passwort')