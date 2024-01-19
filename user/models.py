from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Team(models.Model):
    team_name = models.CharField(max_length=50)
    team_leader = models.OneToOneField(User, on_delete=models.Empty, null=True, related_name='team_name')
    members = models.ManyToManyField(User, related_name='team_members')

    def __str__(self):
        return self.team_name

    def all_members(self):
        members = ''
        for member in self.members.all():
            members += member.first_name + ' ' + member.last_name + ',\r\n'
        return members


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    is_team_leader = models.BooleanField(default=False)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.first_name} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
