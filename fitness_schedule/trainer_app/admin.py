from django.contrib import admin
from .models import Trainer, Gym, Client, Program, Schedule


class TrainerGymInline(admin.TabularInline):
    model = Trainer.gyms.through
    extra = 0


class TrainerScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 0


class GymAdmin(admin.ModelAdmin):
    inlines = [
        TrainerGymInline
    ]


class TrainerAdmin(admin.ModelAdmin):
    exclude = ('gyms',)

    inlines = [
        TrainerScheduleInline
    ]


admin.site.register(Trainer, TrainerAdmin)
admin.site.register(Gym, GymAdmin)
admin.site.register(Client)
admin.site.register(Program)
admin.site.register(Schedule)