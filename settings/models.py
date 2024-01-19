from django.db import models

PROJECT_CAT = [
    ('Land', 'Land'),
    ('Apartment', 'Apartment'),
]


class Project(models.Model):
    project_name = models.CharField(max_length=200)
    project_category = models.CharField(max_length=20, choices=PROJECT_CAT, default='Land')
    project_initial = models.CharField(max_length=4)
    project_location = models.CharField(max_length=500)

    def __str__(self):
        return str(self.project_name)
