from django.contrib import admin
from .models import Service, Appointment, Profile

admin.site.register(Service)
admin.site.register(Appointment)


@admin.register(Profile)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone_number')
    list_filter = ('role',)
    search_fields = ('user__username', 'phone_number')
