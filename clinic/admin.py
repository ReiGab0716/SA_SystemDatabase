from django.contrib import admin
from django.utils.html import format_html
from .models import Service, Appointment, Profile

admin.site.register(Appointment)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'image_preview')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    readonly_fields = ('image_preview',)
    fields = ('name', 'category', 'description', 'price', 'image', 'image_preview')

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="height: 80px; width: 120px; object-fit: cover; border-radius: 8px;" />',
                obj.image.url,
            )
        return "No image uploaded"

    image_preview.short_description = "Photo preview"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone_number', 'profile_image_preview')
    list_filter = ('role',)
    search_fields = ('user__username', 'phone_number')
    readonly_fields = ('profile_image_preview',)

    def profile_image_preview(self, obj):
        if obj and obj.profile_image:
            return format_html(
                '<img src="{}" style="height: 72px; width: 72px; object-fit: cover; border-radius: 50%;" />',
                obj.profile_image.url,
            )
        return "No image uploaded"

    profile_image_preview.short_description = "Profile photo"
