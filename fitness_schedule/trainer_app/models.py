from django.db import models

from django.core.exceptions import ValidationError

from django.contrib.auth.models import User


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Gym(TimestampedModel):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name} - {self.address}'


class Trainer(TimestampedModel):
    GENDER_CHOICES = (
        ('male', 'Мужской'),
        ('female', 'Женский'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    gyms = models.ManyToManyField(Gym, related_name='trainers')

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Client(TimestampedModel):
    GENDER_CHOICES = (
        ('male', 'Мужской'),
        ('female', 'Женский'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Program(TimestampedModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()

    def __str__(self):
        return f'{self.gym} {self.trainer.user.first_name} {self.client.user.first_name}'


class Schedule(TimestampedModel):
    trainer = models.ForeignKey(Trainer, related_name='schedule', on_delete=models.CASCADE)
    gym = models.ForeignKey(Gym, on_delete=models.SET_NULL, null=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()

    def __str__(self):
        return f'{self.start_at} {self.end_at} {self.trainer.user.first_name}'

    def save(self, *args, **kwargs):
        overlapping_schedules = Schedule.objects.filter(
            start_at__lt=self.end_at,
            end_at__gt=self.start_at
        )
        if overlapping_schedules.exists():
            raise ValidationError("Schedule overlaps with existing schedule")

        super().save(*args, **kwargs)

