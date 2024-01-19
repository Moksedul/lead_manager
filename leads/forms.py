from django.contrib.auth.models import User
from django.forms import ModelForm, ModelChoiceField
from django.contrib.admin.widgets import AdminDateWidget

# from core.utils import get_team_members
# from user.models import Team, Profile

from .models import Lead


class UserModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()


class LeadForm(ModelForm):
    assigned_to = UserModelChoiceField(queryset=User.objects.filter(is_staff=False), required=False,
                                       label='assigned_to')
    assigned_member = UserModelChoiceField(queryset=User.objects.filter(is_staff=False), required=False,
                                           label='assigned_member')

    class Meta:
        model = Lead
        fields = '__all__'
        exclude = ('added_by', 'uploaded_time', 'distribution_no', 'last_updated')
        widgets = {
            'created_time': AdminDateWidget(),
            'follow_up_time': AdminDateWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sales_man = User.objects.filter(groups__name='Marketing')
        self.fields['assigned_to'].queryset = sales_man


class LeadFormWeb(ModelForm):
    class Meta:
        model = Lead
        fields = ('full_name', 'phone_number', 'email', 'interested_in', 'descriptions')
        widgets = {
            'created_time': AdminDateWidget(),
            'follow_up_time': AdminDateWidget(),
        }
        labels = {
            'descriptions': 'Queries'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = False


class MemberModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()


class LeadUpdateFormLeader(ModelForm):
    assigned_member = MemberModelChoiceField(queryset=User.objects.filter(is_staff=False), required=False)

    class Meta:
        model = Lead
        fields = '__all__'
        exclude = ('added_by', 'uploaded_time', 'distribution_no', 'last_updated', 'assigned_to')
        widgets = {
            'created_time': AdminDateWidget(),
            'follow_up_time': AdminDateWidget(),
        }
        labels = {
            # 'added_by': 'Seller',
        }

    def __init__(self, *args, **kwargs):
        super(LeadUpdateFormLeader, self).__init__(*args, **kwargs)


class LeadUpdateFormMember(ModelForm):
    class Meta:
        model = Lead
        fields = '__all__'
        exclude = ('added_by', 'uploaded_time', 'distribution_no', 'last_updated', 'assigned_to', 'assigned_member')
        widgets = {
            'created_time': AdminDateWidget(),
            'follow_up_time': AdminDateWidget(),
        }
