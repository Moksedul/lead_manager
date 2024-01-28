from django.urls import path

from core.utils import autocomplete_search_leads
from .views import *

urlpatterns = [

    path('new_lead', LeadCreate.as_view(), name='new-lead'),
    path('new_lead_count', new_leads_count, name='new-lead-count'),
    path('lead_list', LeadList.as_view(), name='lead-list'),
    path('lead_edit/<int:pk>/', lead_update, name='lead-edit'),
    path('lead/<int:pk>/delete', LeadDelete.as_view(), name='delete-lead'),
    path('lead_print', lead_print, name='lead-print'),
    path('lead_edit/assign_member/', assign_member, name='assign-member'),
    path('new_lead_web', LeadCreateWeb.as_view(), name='new-lead-web'),
    path('thank_you', thank_you_page, name='thank-you'),
    path('autocomplete_search_leads', autocomplete_search_leads, name='autocomplete-search-leads'),
    path('lead_update', lead_update_instant, name='lead-update-instant'),

]
