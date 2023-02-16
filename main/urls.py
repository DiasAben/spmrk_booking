from django.urls import path

from .views import (BookingApproveView, BookingCreateWizardView,
                    BookingDeleteView, BookingHomeView, BookingListView,
                    BookingSettingsView)

urlpatterns = [
    path("", BookingCreateWizardView.as_view(), name="create_booking"),
    path("admin/list", BookingListView.as_view(), name="booking_list"),
    path("admin/settings", BookingSettingsView.as_view(), name="booking_settings"),
    path("admin/<pk>/delete",
         BookingDeleteView.as_view(), name="booking_delete"),
    path("admin/<pk>/approve",
         BookingApproveView.as_view(), name="booking_approve"),
]
