from django.db.models import Q
from django.utils import timezone

from .models import Appointment


def count_unique_trns(queryset):
    referenced = queryset.exclude(reference_number__isnull=True).exclude(reference_number="")
    missing_reference = queryset.filter(Q(reference_number__isnull=True) | Q(reference_number=""))
    return referenced.values("reference_number").distinct().count() + missing_reference.values("id").distinct().count()


def staff_notifications(request):
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        return {}

    role = getattr(getattr(user, "profile", None), "role", None)
    if role not in {"DOCTOR", "SECRETARY"}:
        return {}

    today = timezone.localdate()
    pending_appointments = Appointment.objects.filter(
        status="Pending",
        date__gte=today,
    )
    count = count_unique_trns(pending_appointments)

    return {
        "staff_new_appointments_count": count,
    }
