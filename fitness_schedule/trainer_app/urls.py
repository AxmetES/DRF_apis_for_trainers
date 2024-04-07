# my_app/urls.py

from django.urls import path
from .views import GymListAPIView, ScheduleListAPIView, ProgramListAPIView, MakeProgramAPIView

urlpatterns = [
    path('getgymlist/', GymListAPIView.as_view(), name='get_gyms_list'),
    path('getschedulelist/', ScheduleListAPIView.as_view(), name='get_schedule_list'),
    path('getprogramlist/', ProgramListAPIView.as_view(), name='get_program_list'),
    path('makeprogram/', MakeProgramAPIView.as_view(), name='make_program'),
]

