import requests
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone

from Gabes_Portfolio import settings
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
    recaptcha_site_key = settings.GOOGLE_RECAPTCHA_SITE_KEY
    recaptcha_secret_key = settings.GOOGLE_RECAPTCHA_SECRET_KEY

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        company = request.POST.get('subject')
        message = request.POST.get('message')
        recaptcha_response = request.POST.get('g-recaptcha-response')

        if not name or not email or not message or not recaptcha_response:
            messages.error(request, 'All fields are required.')
            return redirect('contact')

        recaptcha_verify_url = 'https://www.google.com/recaptcha/api/siteverify'
        recaptcha_data = {
            'secret': recaptcha_secret_key,
            'response': recaptcha_response
        }
        recaptcha_result = requests.post(recaptcha_verify_url, data=recaptcha_data)
        recaptcha_result_json = recaptcha_result.json()

        recaptcha_score = recaptcha_result_json.get('score', 0)

        if not recaptcha_result_json.get('success') or recaptcha_score < 0.5:
            messages.error(request, 'reCAPTCHA verification failed. Please try again.')
            return redirect('contact')

        email_subject = 'New Contact Submission'
        email_body = render_to_string('contact_email.txt', {
            'name': name,
            'email': email,
            'company': company,
            'message': message,
        })

        email_message = EmailMessage(
            email_subject,
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            ['gstockoption4@gmail.com']
        )

        try:
            email_message.send()
            messages.success(request, 'Thank you for reaching out! I will get back to you shortly!')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

        return redirect('contact')

    return render(request, 'contact.html', {
        'recaptcha_site_key': recaptcha_site_key
    })