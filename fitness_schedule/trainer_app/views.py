# my_app/views.py
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Trainer, Program
from .serializers import ScheduleSerializer, GymSerializer, ProgramSerializer, ProgramCreateSerializer


class GymListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            if hasattr(request.user, 'trainer'):
                trainer = Trainer.objects.get(user=request.user)
                gyms = trainer.gyms.all()
                gym_data = GymSerializer(gyms, many=True)
                return Response(gym_data.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Unknown user type'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ScheduleListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            if hasattr(request.user, 'trainer'):
                trainer = Trainer.objects.get(user=request.user)
                schedules = trainer.schedule.all()
                schedules = ScheduleSerializer(schedules, many=True)
                return Response(schedules.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Unknown user type'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProgramListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            programs = Program.objects.filter(trainer__user=request.user)
            schedules_data = ProgramSerializer(programs, many=True)
            return Response(schedules_data.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MakeProgramAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['client_email', 'gym', 'trainer_email', 'date', 'start_time', 'end_time',],
            properties={
                'client_email': openapi.Schema(type=openapi.TYPE_STRING,
                                               description='Email of the client',
                                               example='calient@mail.ru'),
                'gym': openapi.Schema(type=openapi.TYPE_STRING,
                                      description='Name of the gym',
                                      example='Gold Gym'),
                'trainer_email': openapi.Schema(type=openapi.TYPE_STRING,
                                                description='Email of the trainer',
                                                example='trainer@mail.ru'),
                'date': openapi.Schema(type=openapi.TYPE_STRING,
                                       description='Day date of the program',
                                       example='07.04.2024'),
                'start_time': openapi.Schema(type=openapi.TYPE_STRING,
                                             description='Start time of the program',
                                             example='11:00:00'),
                'end_time': openapi.Schema(type=openapi.TYPE_STRING,
                                           description='End time of the program',
                                           example='12:00:00'),
            }))
    def post(self, request, *args, **kwargs):
        try:
            if hasattr(request.user, 'trainer'):
                serializer = ProgramCreateSerializer(data=request.data)
                if serializer.is_valid():
                    program = serializer.save()
                    serializer = ProgramSerializer(program)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)