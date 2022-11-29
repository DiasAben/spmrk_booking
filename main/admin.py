from django.contrib import admin

from main.models import Booking, BookingSettings


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user_email", "user_name", "date", "training_name", "approved")
    list_filter = ("approved", "date")
    ordering = ("date", "training_name")
    search_fields = ("user_email", "user_name")


admin.site.register(BookingSettings)
