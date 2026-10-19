import datetime
from django.utils import timezone
from datacenter.models import Passcard
from datacenter.models import Visit
from datacenter.models import get_duration, format_duration
from django.shortcuts import render


def storage_information_view(request):
    passcards_not_leaved = Visit.objects.filter(leaved_at=None)
    non_closed_visits = []
    today = timezone.now()
    for visit in passcards_not_leaved:
        duration = get_duration(visit)
        time_in_storage = format_duration(duration)
        visitor = {
                'who_entered': visit.passcard.owner_name,
                'entered_at': timezone.localtime(visit.entered_at),
                'duration': time_in_storage,
        }
        non_closed_visits.append(visitor)

    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
