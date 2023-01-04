import requests
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect

from .forms import *
from .utils import *


menu = [{'title': "Ввід даних", 'url_name': 'add_data'},
        {'title': "Перегляд даних", 'url_name': 'show_data'},
        {'title': "Звіт", 'url_name': 'make_report'},
        {'title': "Новини", 'url_name': 'news'},
        ]


def home(request):
    context = {
        'menu': menu,
        'title': ''
    }
    return render(request, 'air/index.html', context)


def api_data(post, item):
    token = '40167071ec38218ceeaf8b7ed4e275be132f676b'
    url = 'https://api.waqi.info/feed/{}/?token=' + token

    cities_dict = {
        'Київ': 'Kyiv',
        'Одеса': 'Odessa',
    }
    pollutants_dict = {
        'PM2.5': 'pm25',
    }

    res = requests.get(url.format(cities_dict[str(post.city)])).json()
    pollutant = pollutants_dict['PM2.5']
    sensor_name = res["data"]["attributions"][1]["name"]

    items_info = {
        'concentration': res["data"]["iaqi"][pollutant]["v"],
        'sensor': Sensor.objects.get(name=sensor_name),
    }

    value = items_info[item]

    return value


def add_data(request):
    context = {
        'menu': menu,
        'title': ''
    }
    return render(request, 'air/add_data.html', context)


def add_my_data(request):
    if request.method == 'POST':
        form = MyDataForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect(request.path)
    else:
        form = MyDataForm()

    context = {
        'menu': menu,
        'title': 'Новий запис',
        'form': form,
    }
    return render(request, 'air/add_my_data.html', context)


def add_sensor_data(request):
    if request.method == 'POST':
        form = SensorDataForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.concentration = api_data(post, 'concentration')
            post.author = request.user
            post.sensor = api_data(post, 'sensor')
            post.save()
            return HttpResponseRedirect(request.path)
    else:
        form = SensorDataForm()

    context = {
        'menu': menu,
        'title': 'Новий запис',
        'form': form,
    }

    return render(request, 'air/add_sensor_data.html', context)


def show_data(request):
    data = AirData.objects.all()

    if len(data) == 0:
        return HttpResponseNotFound('<h1>Дані відсутні</h1>')

    context = {
        'menu': menu,
        'title': '',
        'data': data,
    }
    return render(request, "air/show_data.html", context)


def make_report(request):
    context = {
        'menu': menu,
        'title': '',
    }
    return render(request, 'air/make_report.html', context)


def year_report(request):
    if request.method == 'GET':
        form = YearReportForm(request.GET)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = YearReportForm()

    context = {
        'menu': menu,
        'title': 'Річний звіт',
        'form': form
    }
    return render(request, 'air/year_report.html', context)


def year_chart(request):
    context = {
        'menu': menu,
        'title': '',
    }
    return render(request, 'air/year_chart.html', context)


def get_year_data(request):
    dates = []
    quantities = []
    city = request.GET.get('city')
    pollutant = request.GET.get('pollutant')
    year = int(request.GET.get('year'))
    period_data = AirData.objects.filter(
        datetime__gte=datetime.datetime(year, 1, 1), datetime__lte=datetime.datetime(year, 12, 31),
        pollutant=pollutant, city=city)
    for item in period_data:
        dates.append(datetime.datetime.strftime(item.datetime, '%d.%m.%Y'))
        quantities.append(item.concentration)

    context = {
        'menu': menu,
        'title': '',
        'labels': dates,
        'data': quantities,
    }
    return render(request, 'air/year_chart.html', context)


def month_report(request):
    context = {
        'menu': menu,
        'title': '',
    }
    return render(request, 'air/year_chart.html', context)


def quarterly_report(request):
    context = {
        'menu': menu,
        'title': '',
    }
    return render(request, 'air/year_chart.html', context)


def news(request):
    posts = News.objects.all()
    if len(posts) == 0:
        return HttpResponseNotFound('<h1>Дані відсутні</h1>')

    context = {
        'menu': menu,
        'title': '',
        'posts': posts
    }
    return render(request, 'air/news.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponseRedirect(request.path)
    else:
        form_class = LoginUserForm()

        context = {
            'form': form_class,
        }
        return render(request, 'air/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Сторінку не знайдено</h1>')
