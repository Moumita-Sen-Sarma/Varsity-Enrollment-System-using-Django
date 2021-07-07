from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

from django import forms
from django.utils.translation import ugettext_lazy as _


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'dept', 'userRole']

admin.site.register(CustomUser, CustomUserAdmin)






class UserCreationFormExtended(CustomUserCreationForm): 
    def __init__(self, *args, **kwargs): 
        super(UserCreationFormExtended, self).__init__(*args, **kwargs) 
        self.fields['dept'] = forms.CharField(label=_("Department"), max_length=75)

CustomUserAdmin.add_form = UserCreationFormExtended
CustomUserAdmin.add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('dept', 'userRole', 'username', 'password1', 'password2',)
    }),
)

admin.site.unregister(CustomUser)
admin.site.register(CustomUser, CustomUserAdmin)



