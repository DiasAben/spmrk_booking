from django.contrib import admin

from main.models import Booking, BookingSettings


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user_email", "user_name", "date", "training_name", "approved", "created_at")
    list_filter = ("approved", "date", "created_at")
    ordering = ("date", "training_name", "created_at")
    search_fields = ("user_email", "user_name")


admin.site.register(BookingSettings)
