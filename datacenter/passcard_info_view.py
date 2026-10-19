import datetime
from django.utils import timezone
from datacenter.models import Passcard
from datacenter.models import Visit
from datacenter.models import get_duration, format_duration, is_visit_long
from django.shortcuts import render, get_object_or_404


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    passcard_visits = Visit.objects.filter(passcard=passcard)
    this_passcard_visits = []
    today = timezone.now()
    for visit in passcard_visits:
        duration = get_duration(visit)
        time_in_storage = format_duration(duration)
        is_strange_flag = is_visit_long(visit)
        visitor = {
                'entered_at': timezone.localtime(visit.entered_at),
                'duration': time_in_storage,
                'is_strange': is_strange_flag
        }
        this_passcard_visits.append(visitor)

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)