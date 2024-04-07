from datetime import datetime

from rest_framework import serializers
from .models import Schedule, Gym, Program, Trainer, Client


class ScheduleSerializer(serializers.ModelSerializer):
    trainer = serializers.SerializerMethodField()
    gym_address = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = ['trainer', 'gym_address', 'start_at', 'end_at']

    def get_trainer(self, obj):
        return obj.trainer.user.first_name

    def get_gym_address(self, obj):
        return f"{obj.gym.name} {obj.gym.address}"


class GymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = ['name', 'address']


class ProgramSerializer(serializers.ModelSerializer):
    trainer = serializers.SerializerMethodField()
    client = serializers.SerializerMethodField()
    gym_address = serializers.SerializerMethodField()
    start_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M', source='start_at')
    end_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M', source='end_at')

    class Meta:
        model = Program
        fields = ['trainer', 'client', 'gym_address', 'start_time', 'end_time']

    def get_trainer(self, obj):
        return obj.trainer.user.first_name

    def get_client(self, obj):
        return obj.client.user.first_name

    def get_gym_address(self, obj):
        return f"{obj.gym.name} {obj.gym.address}"


class ProgramCreateSerializer(serializers.ModelSerializer):
    client_email = serializers.EmailField()
    trainer_email = serializers.EmailField()
    gym = serializers.CharField(max_length=100)
    date = serializers.CharField()
    start_time = serializers.CharField()
    end_time = serializers.CharField()


    class Meta:
        model = Program
        fields = ['client_email', 'trainer_email', 'gym', 'date', 'start_time', 'end_time']

    def validate_client_email(self, value):
        try:
            client = Client.objects.get(user__email=value)
        except Client.DoesNotExist:
            raise serializers.ValidationError("Client does not exist.")
        return client

    def validate_trainer_email(self, value):
        try:
            trainer = Trainer.objects.get(user__email=value)
        except Trainer.DoesNotExist:
            raise serializers.ValidationError("Trainer does not exist.")
        return trainer

    def validate_gym(self, value):
        try:
            gym = Gym.objects.get(name=value)
        except Gym.DoesNotExist:
            raise serializers.ValidationError("Gym does not exist.")
        return gym

    def create(self, validated_data):
        client = validated_data.pop('client_email')
        trainer = validated_data.pop('trainer_email')
        gym = validated_data.pop('gym')
        date_str = validated_data.pop('date')
        start_time_str = validated_data.pop('start_time')
        end_time_str = validated_data.pop('end_time')

        date = datetime.strptime(date_str, '%d.%m.%Y').date()
        start_time = datetime.strptime(start_time_str, '%H:%M:%S').time()
        end_time = datetime.strptime(end_time_str, '%H:%M:%S').time()

        start_datetime = datetime.combine(date, start_time)
        end_datetime = datetime.combine(date, end_time)

        program = Program.objects.create(client=client, trainer=trainer, gym=gym, start_at=start_datetime,
                                         end_at=end_datetime, **validated_data)
        return program


class ClientSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)

    class Meta:
        model = Client
        fields = ['first_name']


class TrainerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)

    class Meta:
        model = Trainer
        fields = ['first_name']


class GymSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gym
        fields = ['name', 'address']


class ProgramSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    trainer = TrainerSerializer()
    gym = GymSerializer()

    class Meta:
        model = Program
        fields = ['id', 'client', 'trainer', 'gym', 'start_at', 'end_at']
