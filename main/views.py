import json
from datetime import date, timedelta

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from webpush import send_user_notification

from leads.models import Lead


@login_required()
def home(request):
    leads = Lead.objects.filter(uploaded_time__range=[(date.today() - timedelta(days=30)), date.today()]).order_by('-id')[:15]
    webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
    vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
    user = request.user
    context = {
        'tittle': 'Lead Manager | Home',
        user: user,
        'vapid_key': vapid_key,
        'leads': leads
    }
    return render(request, 'main/home.html', context)


@login_required()
def person_load(request):
    persons = User.objects.filter(is_superuser=False)
    context = {
        'persons': persons
    }
    return render(request, 'main/notification_form.html', context=context)


@require_POST
@csrf_exempt
def send_push(request):
    body = request.body
    data = json.loads(body)

    user_id = data['user']
    user = User.objects.get(id=user_id)
    payload = {'head': 'New Message', 'body': data['body']}
    print('ok')
    print(send_user_notification(user=user.id, payload=payload, ttl=1000))
    return JsonResponse(status=200, data={"message": "Web push successful"})


@login_required()
def notification_allow(request):
    context = {

    }
    return render(request, 'main/notification_subscription.html', context=context)
