import datetime
import json
import logging
from typing import Dict, List

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, ListView, TemplateView, UpdateView, View
from formtools.wizard.views import SessionWizardView
from django.views.generic import FormView
from main.forms import BookingCustomerForm, BookingDateForm, BookingSettingsForm
from main.models import Booking, BookingSettings
from main.settings import BOOKING_BG, BOOKING_DESC, BOOKING_DISABLE_URL, BOOKING_SUCCESS_REDIRECT_URL, BOOKING_TITLE, PAGINATION
from main.utils import BookingSettingMixin


# # # # # # #
# Admin Part
# # # # # # #
class BookingHomeView(BookingSettingMixin, TemplateView):
    model = Booking
    template_name = "booking/admin/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["last_bookings"] = Booking.objects.order_by("date", "time")[:10]
        context["waiting_bookings"] = Booking.objects.filter(approved=False).order_by("-date", "time")[:10]
        return context


class BookingListView(BookingSettingMixin, ListView):
    model = Booking
    template_name = "booking/admin/booking_list.html"
    paginate_by = PAGINATION


class BookingSettingsView(BookingSettingMixin, UpdateView):
    form_class = BookingSettingsForm
    template_name = "booking/admin/booking_settings.html"

    def get_object(self):
        queryset = BookingSettings.objects.all()
        if queryset.exists():
            return queryset.first()
        return None

    def get_success_url(self):
        return reverse("booking_settings")


class BookingDeleteView(BookingSettingMixin, DeleteView):
    model = Booking
    success_url = reverse_lazy("booking_list")
    queryset = Booking.objects.all()


class BookingApproveView(BookingSettingMixin, View):
    model = Booking
    success_url = reverse_lazy("booking_list")
    fields = ("approved",)

    def post(self, request, *args, **kwargs):
        booking = get_object_or_404(Booking, pk=self.kwargs.get("pk"))
        booking.approved = True
        booking.save()

        return redirect(self.success_url)


# # # # # # # #
# Booking Part
# # # # # # # #
BOOKING_STEP_FORMS = (("Date", BookingDateForm),)


class BookingCreateWizardView(SessionWizardView):
    template_name = "booking/user/main_page.html"
    form_list = BOOKING_STEP_FORMS

    def get_context_data(self, form: FormView, **kwargs: Dict) -> Dict:
        context = super().get_context_data(form=form, **kwargs)
        demo = BookingSettings.objects.all()
        demo1 = {}
        for bookings in demo:
            bookingnum = bookings.booking_set.all()
            if bookingnum.count() <= 15:
                demo1[str(bookings.training_date)] = bookings.training_name
        dvalues = list(demo1.values())
        dvalues = [*set(dvalues)]
        svalues = {}
        for i in dvalues:
            svalues[i] = [k for k, v in demo1.items() if v in i]
        logging.info(svalues)
        context["demo"] = json.dumps(svalues, ensure_ascii=False)
        context.update({
            'booking_settings': get_object_or_404(BookingSettings, pk=1),
            "booking_bg": BOOKING_BG,
            "description": BOOKING_DESC,
            "title": BOOKING_TITLE
        })
        return context

    def render(self, form: FormView, **kwargs: Dict) -> render:
        # Check if Booking is Disable
        form = form or self.get_form()
        context = self.get_context_data(form=form, **kwargs)

        if not context["booking_settings"].booking_enable:
            return redirect(BOOKING_DISABLE_URL)
        return self.render_to_response(context)

    def done(self, form_list: List[FormView], **kwargs: Dict) -> redirect:
        data = {key: value for form in form_list for key, value in form.cleaned_data.items()}
        training_name = data.get('email')
        del data['email']
        training = get_object_or_404(BookingSettings, training_date=data["date"], training_name=training_name)
        data['training_name_id'] = training.id
        booking = Booking.objects.create(**data)

        if BOOKING_SUCCESS_REDIRECT_URL:
            return redirect(BOOKING_SUCCESS_REDIRECT_URL)

        return render(self.request, 'booking/user/booking_done.html', {
            "progress_width": "100",
            "booking_id": booking.id,
            "booking_bg": BOOKING_BG,
            "description": BOOKING_DESC,
            "title": BOOKING_TITLE
        })


def add_delta(time: datetime.time, delta: datetime.datetime) -> datetime.time:
    # transform to a full datetime first
    return (datetime.datetime.combine(
        datetime.date.today(), time
    ) + delta).time()


def get_available_time(date: datetime.date) -> List[Dict[datetime.time, bool]]:
    """
    Check for all available time for selected date
    The times should ne betwwen start_time and end_time
    If the time already is taken -> is_taken = True
    """
    booking_settings = BookingSettings.objects.filter(training_date=date)
    existing_bookings = Booking.objects.filter(
        date=date).values_list('time')

    next_time = booking_settings[0].start_time
    time_list = []
    while True:
        is_taken = any([x[0] == next_time for x in existing_bookings])
        time_list.append(
            {"time": ":".join(str(next_time).split(":")[:-1]), "is_taken": is_taken})
        next_time = add_delta(next_time, datetime.timedelta(
            minutes=int(booking_settings[0].period_of_each_booking)))
        if next_time > booking_settings[0].end_time:
            break
    return time_list
