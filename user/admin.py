from django import forms
from django.contrib import admin
from django.contrib.auth.models import User, Group

from .models import Profile, Team
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'team_leader', 'all_members')


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def clean_is_superuser(self):
        is_superuser = self.cleaned_data.get('is_superuser')
        if is_superuser and not self.request.user.is_superuser:
            raise forms.ValidationError("Only superusers can assign superuser status.")
        return is_superuser


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

    def clean_is_superuser(self):
        is_superuser = self.cleaned_data.get('is_superuser')
        if is_superuser and not self.request.user.is_superuser:
            raise forms.ValidationError("Only superusers can assign superuser status.")
        return is_superuser


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            form = CustomUserCreationForm
        else:
            form = CustomUserChangeForm

        # Pass the request object to the form
        form.request = request
        return form

    def get_queryset(self, request):
        # Exclude superusers from the queryset
        qs = super().get_queryset(request)
        return qs.filter(is_superuser=False)

    def has_delete_permission(self, request, obj=None):
        # Prevent other users from deleting superusers
        if obj and obj.is_superuser and not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        # Prevent other users from changing superuser details
        if obj and obj.is_superuser and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    def has_view_permission(self, request, obj=None):
        # Prevent other users from seeing superuser details
        if obj and obj.is_superuser and not request.user.is_superuser:
            return False
        return super().has_view_permission(request, obj)

    def get_fieldsets(self, request, obj=None):
        print(obj)
        if not obj:
            # default fieldsets for new user create
            fieldsets = super().get_fieldsets(request, obj)
        else:
            # If the current user is a superuser, show all fields
            if request.user.is_superuser:
                fieldsets = (
                    (None, {'fields': ('username', 'password')}),
                    ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
                    ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
                    ('Important dates', {'fields': ('last_login', 'date_joined')}),
                )
            elif request.user.has_perm('auth.change_permission'):
                # For staff users, show a limited set of fields
                fieldsets = (
                    (None, {'fields': ('username', 'password')}),
                    ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
                    ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
                )
            else:
                # For staff users, show a limited set of fields
                fieldsets = (
                    (None, {'fields': ('username', 'password')}),
                    ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
                )
        return fieldsets


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Profile)
admin.site.register(Team, TeamAdmin)

