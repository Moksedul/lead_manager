from leads.models import Lead
from itertools import chain
from django.http import JsonResponse


def autocomplete_search_leads(request):
    if request.user.is_staff:
        leads = Lead.objects.all()
    else:
        leads = Lead.objects.filter(assigned_to=request.user)
    data = []

    if 'term' in request.GET:
        term = request.GET.get('term')
        qs1 = leads.filter(full_name__contains=term)
        qs2 = leads.filter(phone_number__contains=term)
        qs3 = leads.filter(email__contains=term)
        data1 = [item.full_name for item in qs1]
        data2 = [item.phone_number for item in qs2]
        data3 = [item.email for item in qs3]
        data = list(chain(data1, data2, data3))
    return JsonResponse(data, safe=False)