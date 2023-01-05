from django.urls import path
from .views import *

urlpatterns = [
    path('', AirHome.as_view(), name='home'),
    path('add_data/', AddData.as_view(), name='add_data'),
    path('add_data/my_data/', AddMyData.as_view(), name='add_my_data'),
    path('add_data/sensor_data/', AddSensorData.as_view(), name='add_sensor_data'),
    path('show_data/', ShowData.as_view(), name='show_data'),
    path('make_report/', MakeReport.as_view(), name='make_report'),
    path('make_report/year_report', YearReportData.as_view(), name='year_report'),
    path('make_report/month_report', MonthReportData.as_view(), name='month_report'),
    path('make_report/quarterly_report', QuarterlyReportData.as_view(), name='quarterly_report'),
    path('make_report/year_report/year_chart', year_chart, name='year_chart'),
    path('news/', AirNews.as_view(), name='news'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]


