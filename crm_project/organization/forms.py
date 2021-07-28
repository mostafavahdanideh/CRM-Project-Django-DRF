from django import forms
from . import models

class AddOrganizationForm(forms.ModelForm):
    class Meta:
        model = models.Organization
        fields = [
            'province',
            'organization_name',
            'organization_phone_number',
            'workers_size',
            'manufacturedـproducts',
            'owner_first_name',
            'owner_last_name',
            'owner_second_last_name',
            'owner_phone_number',
            'owner_email',
            
        ]