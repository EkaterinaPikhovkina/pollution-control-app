import requests
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView

from .forms import *
from .utils import *


menu = [{'title': "Ввід даних", 'url_name': 'add_data'},
        {'title': "Перегляд даних", 'url_name': 'show_data'},
        {'title': "Звіт", 'url_name': 'make_report'},
        {'title': "Новини", 'url_name': 'news'},
        ]


class AirHome(DataMixin, TemplateView):
    template_name = 'air/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Головна")
        return dict(list(context.items()) + list(c_def.items()))


class AddData(DataMixin, TemplateView):
    template_name = 'air/add_data.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Додати дані")
        return dict(list(context.items()) + list(c_def.items()))


class AddMyData(DataMixin, CreateView):
    form_class = MyDataForm
    template_name = 'air/add_my_data.html'
    success_url = reverse_lazy('add_my_data')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        if self.object.concentration > self.object.pollutant.norm_ind:
            news = News()
            news.advice = Advice.objects.get(pollutant_id=self.object.pollutant.id)
            news.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новий запис'
        context['menu'] = menu
        return context

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(AddMyData, self).get_form_kwargs(*args, **kwargs)
        kwargs['author'] = self.request.user
        return kwargs


class AddSensorData(DataMixin, CreateView):
    form_class = SensorDataForm
    template_name = 'air/add_sensor_data.html'
    success_url = reverse_lazy('add_sensor_data')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.concentration = self.api_data(self.object, 'concentration')
        if self.object.concentration > self.object.pollutant.norm_ind:
            news = News()
            news.advice = Advice.objects.get(pollutant_id=self.object.pollutant.id)
            news.save()
        self.object.sensor = self.api_data(self.object, 'sensor')
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новий запис'
        context['menu'] = menu
        return context

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(AddSensorData, self).get_form_kwargs(*args, **kwargs)
        kwargs['author'] = self.request.user
        return kwargs

    def api_data(self, post, item):
        token = '40167071ec38218ceeaf8b7ed4e275be132f676b'
        url = 'https://api.waqi.info/feed/{}/?token=' + token

        res = requests.get(url.format(post.city.api_name)).json()
        pollutant = post.pollutant.api_name
        sensor_name = res["data"]["attributions"][1]["name"]

        items_info = {
            'concentration': res["data"]["iaqi"][pollutant]["v"],
            'sensor': Sensor.objects.get(name=sensor_name),
        }

        value = items_info[item]

        return value


class ShowData(DataMixin, ListView):
    model = AirData
    template_name = 'air/show_data.html'
    context_object_name = 'data'
    # paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Дані по забрудненню")
        return dict(list(context.items()) + list(c_def.items()))


class MakeReport(DataMixin, TemplateView):
    template_name = 'air/make_report.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Звіт")
        return dict(list(context.items()) + list(c_def.items()))


class YearReportData(DataMixin, CreateView):
    form_class = YearReportForm
    template_name = 'air/year_report.html'
    success_url = reverse_lazy('year_chart')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Річний звіт'
        context['menu'] = menu
        return context


class MonthReportData(DataMixin, CreateView):
    form_class = MonthReportForm
    template_name = 'air/month_report.html'
    success_url = reverse_lazy('year_chart')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Місячний звіт'
        context['menu'] = menu
        return context


class QuarterlyReportData(DataMixin, CreateView):
    form_class = QuarterlyReportForm
    template_name = 'air/quarterly_report.html'
    success_url = reverse_lazy('year_chart')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Квартальний звіт'
        context['menu'] = menu
        return context


def year_chart(request):
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
        'title': 'Річний графік',
        'labels': dates,
        'data': quantities,
    }
    return render(request, 'air/year_chart.html', context)


class AirNews(DataMixin, ListView):
    model = News
    template_name = 'air/news.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Новини")
        return dict(list(context.items()) + list(c_def.items()))


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
            'title': 'Авторизація',
        }
        return render(request, 'air/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Сторінку не знайдено</h1>')
