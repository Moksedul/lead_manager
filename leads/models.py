import re
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

LEAD_STATUS = [
    ('Normal', 'Normal'),
    ('Prospective', 'Prospective'),
    ('Visited', 'Visited'),
    ('Confirmed', 'Confirmed'),
    ('Sold', 'Sold'),
    ('Bad', 'Bad'),
]

LEAD_STATUS_T = ['Normal', 'Prospective', 'Visited', 'Confirmed', 'Sold', 'Bad']

CONTACT_T = ['No', 'Yes']

CONTACT = [
    ('No', 'No'),
    ('Yes', 'Yes'),
]


def interest_choices():
    from settings.models import Project
    interests = [
        ('Land', 'Land'),
        ('Apartment', 'Apartment'),
    ]
    projects = Project.objects.all()
    for project in projects:
        project_option = (project.project_name, project.project_name)
        interests.append(project_option)
    return interests


class Lead(models.Model):
    distribution_no = models.IntegerField(blank=True, null=True)
    lead_source = models.CharField(max_length=50)
    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100)
    interested_in = models.CharField(choices=interest_choices(), max_length=20, default='Land')
    uploaded_time = models.DateTimeField(default=now, null=True, blank=True)
    created_time = models.DateField(default=now)
    follow_up_time = models.DateField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    descriptions = models.TextField(max_length=500, null=True, blank=True)
    contacted = models.CharField(max_length=10, choices=CONTACT, default='No')
    status = models.CharField(max_length=20, choices=LEAD_STATUS, default='Normal')
    added_by = models.ForeignKey(User, on_delete=models.Empty, null=True, blank=True, related_name='added_by')
    assigned_to = models.ForeignKey(User, on_delete=models.Empty, blank=True, null=True, related_name='assigned_to')
    assigned_member = models.ForeignKey(User, on_delete=models.Empty, blank=True, null=True,
                                        related_name='assigned_member')

    def __str__(self):
        return str(self.full_name)

    @property
    def email_valid(self):
        email = str(self.email)
        valid = bool(re.match("([^@|\s]+@[^@]+\.[^@|\s]+)", email))
        return valid

    @staticmethod
    def get_absolute_url():
        return reverse('lead-list')
