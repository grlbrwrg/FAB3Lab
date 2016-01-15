from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
import datetime
from models import Walter


# Create your views here.

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def tagesfarbe():
    zeit = datetime.datetime.now()
    r = zeit.second*3
    g = 100+zeit.minute*2
    b = zeit.hour*5
    rgb = r,g,b
    return rgb

def simple(request):
    import random
    import django
    import datetime

    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    fig=Figure(figsize=(5,5), dpi=80)
    ax=fig.add_subplot(111)
    x=[]
    y=[]
    now=datetime.datetime.now()
    delta=datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now+=delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    response=django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

def index(request):

    return render(request,'hilde/index.html',{'farbe':rgb_to_hex(tagesfarbe())})
    
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
    
def hildeAPI(request):
    if request.GET:
        data = request.GET
        key = data.get('k')
        if int(key) == 1:
            
            
            return HttpResponse('LALALA')
        return HttpResponse(key)
    else:
        return HttpResponseRedirect('/')