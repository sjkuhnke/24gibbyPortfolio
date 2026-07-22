from django.shortcuts import render
from django.utils import timezone

from .models import Show


def home(request):
    upcoming_shows = Show.objects.filter(date__gte=timezone.now().date()).order_by('date')
    context = {
        'upcoming_shows': upcoming_shows,
    }
    return render(request, 'home.html', context)


def shows(request):
    today = timezone.now().date()
    upcoming_shows = Show.objects.filter(date__gte=today).order_by('date')
    past_shows = Show.objects.filter(date__lt=today).order_by('-date')

    shows_by_month = {}
    for show in upcoming_shows:
        month_label = show.date.strftime('%B %Y')
        shows_by_month.setdefault(month_label, []).append(show)

    context = {
        'shows_by_month': shows_by_month,
        'past_shows': past_shows,
    }
    return render(request, 'shows.html', context)


def merch(request):
    return render(request, 'merch.html')


def contact(request):
    return render(request, 'contact.html')