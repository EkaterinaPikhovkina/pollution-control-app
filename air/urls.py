from django.conf.urls.static import static
from django.urls import path
from .views import *
from ..AirApp import settings

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_user, name='login'),
    path('add_data/', add_data, name='add_data'),
    path('add_data/my_data/', add_my_data, name='add_my_data'),
    path('add_data/sensor_data/', add_sensor_data, name='add_sensor_data'),
    path('show_data/', show_data, name='show_data'),
    path('make_report/', make_report, name='make_report'),
    path('make_report/year_report', year_report, name='year_report'),
    path('make_report/year_report/year_chart', get_year_data, name='year_chart'),
    path('make_report/month_report', month_report, name='month_report'),
    path('make_report/quarterly_report', quarterly_report, name='quarterly_report'),
    path('logout/', logout_user, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound

