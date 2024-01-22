
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView
from core.notifications import send_notification
from core.utils import get_team_members
from user.models import Team, Profile

from .forms import *
from .models import Lead, LEAD_STATUS_T, CONTACT_T
from django.contrib.auth.models import User


def new_leads_count(request):
    user = request.user
    leads = Lead.objects.filter(contacted='No')
    if user.has_perm('lead.delete_lead'):
        leads = leads
    else:
        leads = leads.filter(Q(assigned_to=user) | Q(assigned_member=user))

    new_leads = leads.count()
    context = {
        'new_lead': new_leads
    }
    return render(request, 'lead/new_lead_count.html', context=context)


class LeadCreate(LoginRequiredMixin, CreateView):
    form_class = LeadForm
    template_name = 'lead/lead_form.html'
    pk = None

    def form_valid(self, form):
        # user = str(self.request.user)
        staff = self.request.user.is_staff
        if staff is not True:
            form.instance.assigned_to = self.request.user
            form.instance.assigned_member = self.request.user
        form.instance.added_by = self.request.user
        item = form.save()
        self.pk = item.pk

        if item.assigned_to:
            user_id = item.assigned_to.id
            data = {
                'head': 'New Lead Added',
                'body': 'Name: ' + item.full_name + ' Phone: ' + item.phone_number,
                'url': '',
                'user': user_id,
            }
            send_notification(data)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'New Lead'
        context['button_name'] = 'Save'
        context['tittle'] = 'New Lead'
        return context

    def get_success_url(self):

        return reverse("lead-list")


@login_required
def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    user = request.user
    try:
        team = Team.objects.get(team_leader=user)
    except Team.DoesNotExist:
        team = None
    leader = team
    if request.method == 'POST':
        if user.is_superuser:
            form = LeadForm(request.POST, instance=lead)
        elif leader:
            form = LeadUpdateFormLeader(request.POST, instance=lead)
        else:
            form = LeadUpdateFormMember(request.POST, instance=lead)

        if form.is_valid():
            form.save()
            return redirect('lead-list')

    else:
        if user.is_superuser:
            form = LeadForm(instance=lead)
        elif leader:
            form = LeadUpdateFormLeader(instance=lead)
        else:
            form = LeadUpdateFormMember(instance=lead)

    context = {
        'form': form,
        'form_name': 'Update Lead',
        'button_name': 'Update',
        'tittle': 'Update Lead',
    }

    return render(request, 'lead/lead_form.html', context)


@login_required()
def lead_update_instant(request):
    data = {'okk': 'idd'}
    if request.method == 'POST':
        lead_id = (request.POST.get('id')).split('-')[-1]
        data_type = (request.POST.get('type'))
        value = (request.POST.get('value'))
        lead = Lead.objects.get(id=lead_id)
        print(lead_id, value, data_type)

        if data_type == 'f_date':
            lead.follow_up_time = value
        elif data_type == 'description':
            lead.descriptions = value
        elif data_type == 'status':
            lead.status = value
        elif data_type == 'contacted':
            lead.contacted = value

        lead.save()
        data = {

        }
    return JsonResponse(data)


class LeadList(LoginRequiredMixin, ListView):
    model = Lead
    template_name = 'lead/lead_list.html'
    context_object_name = 'Leads'
    ordering = 'distribution_no'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        permission = user.has_perm('lead.delete_lead')
        admin = user.is_staff
        try:
            team = Team.objects.get(team_leader=user)
        except Team.DoesNotExist:
            team = None
        leader = team

        if admin and leader:
            staffs = User.objects.all()
        elif leader:
            staffs = team.members.all()
        else:
            staffs = User.objects.filter(id=user.id)

        search_contains = self.request.GET.get('lead_search')
        search_value = ''
        if search_contains is None or search_contains == '':
            search_contains = 'type to search'
        else:
            search_value = search_contains

        staff_contains = self.request.GET.get('staff')
        if staff_contains is None or staff_contains == '':
            staff_contains = 'Select Staff'
        else:
            staff_contains = User.objects.get(id=staff_contains)

        distribution_contains = self.request.GET.get('distribution')
        dn_value = ''
        if distribution_contains is None or distribution_contains == '':
            distribution_contains = 'Type Distribution'
        else:
            dn_value = distribution_contains
        today = now()

        need_to_follow_up = 0
        members = get_team_members(user)

        context['members'] = members
        context['need_to_follow_up'] = need_to_follow_up
        context['distribution_selected'] = distribution_contains
        context['search_contains'] = search_contains
        context['tittle'] = 'Lead List'
        context['admin'] = admin
        context['leader'] = leader
        context['today'] = today
        context['permission'] = permission
        context['staffs'] = staffs
        context['staff_selected'] = staff_contains
        context['dn_value'] = dn_value
        context['search_value'] = search_value
        context['status_options'] = LEAD_STATUS_T
        context['contact_options'] = CONTACT_T

        return context

    def get_queryset(self):
        user = self.request.user
        admin = user.is_staff

        if not admin:
            profile = Profile.objects.get(user=user)
            if profile.is_team_leader:
                leads = Lead.objects.filter(assigned_to=user)\
                    .order_by('contacted', '-follow_up_time', '-uploaded_time', 'last_updated', 'contacted',)
            else:
                leads = Lead.objects.filter(Q(assigned_to=user) | Q(assigned_member=user))\
                    .order_by('contacted', '-follow_up_time', '-uploaded_time', 'contacted',)
        else:
            if self.request.user.has_perm('lead.delete_lead'):
                leads = Lead.objects.all()\
                    .order_by('contacted', '-follow_up_time', '-uploaded_time', 'contacted',)
            else:
                leads = Lead.objects.none()

        distribution_contains = self.request.GET.get('distribution')
        search_contains = self.request.GET.get('lead_search')
        staff_contains = self.request.GET.get('staff')

        if search_contains != '' and search_contains is not None:
            leads_with_name = leads.filter(full_name__contains=search_contains)

            if leads_with_name.exists():
                leads = leads_with_name
            else:
                leads_with_phone = leads.filter(phone_number__contains=search_contains)
                if leads_with_phone.exists():
                    leads = leads_with_phone
                else:
                    leads = leads.filter(email__contains=search_contains)

        if staff_contains is not None and staff_contains != '':
            leads = leads.filter(Q(assigned_to=staff_contains) | Q(assigned_member=staff_contains))

        if distribution_contains is not None and distribution_contains != '':
            leads = leads.filter(distribution_no=distribution_contains)

        return leads


@login_required()
def lead_print(request):
    leads = Lead.objects.all()
    description = request.GET.get('description')
    dn_no = request.GET.get('d_number')
    member = request.GET.get('member')
    admin = request.user.is_staff

    if dn_no != '' and dn_no is not None:
        leads = leads.filter(distribution_no=dn_no)

    else:
        dn_no = 'ALL'

    if admin:
        user = User.objects.get(id=member)
        leads = leads.filter(assigned_member=user)
    else:
        user = User.objects.get(id=request.user.id)
        leads = leads.filter(assigned_member=user)
    context = {
        'tittle': 'Lead print',
        'leads': leads,
        'description': description,
        'dn_no': dn_no,
        'r_user': user
    }

    return render(request, 'lead/lead_print.html', context)


@login_required()
def assign_member(request):

    selected_leads = request.POST.getlist('selected_leads')
    selected_member = request.POST.get('selected_member')

    for lead_id in selected_leads:
        lead = Lead.objects.get(id=lead_id)
        if selected_member != '':
            user = User.objects.get(id=selected_member)
            lead.assigned_member = user
        else:
            lead.assigned_member = None

        lead.save()

    return redirect(Lead)


class CSRFExemptMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptMixin, self).dispatch(*args, **kwargs)


class LeadCreateWeb(CSRFExemptMixin, CreateView):
    form_class = LeadFormWeb
    template_name = 'lead/lead_form_web.html'

    def form_valid(self, form):
        users = User.objects.filter(is_staff=True)
        form.instance.lead_source = 'Website'
        item = form.save()
        for user in users:
            user_id = user.id
            data = {
                'head': 'New Lead Added',
                'body': 'Name: ' + item.full_name + ' Phone: ' + item.phone_number,
                'url': '',
                'user': user_id,
            }
            send_notification(data)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'SEND US YOUR REQUIREMENT'
        context['button_name'] = 'Submit'
        context['title'] = '.'
        return context

    def get_success_url(self):

        return reverse("thank-you")


def thank_you_page(request):
    message = "Thanks a bunch for filling that out. " \
              "It means a lot to us, just like you do! We will contact you very soon."

    context = {
        'message': message
    }
    return render(request, 'lead/thank_you_page.html', context)


