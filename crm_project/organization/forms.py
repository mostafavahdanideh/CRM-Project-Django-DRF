from django import forms
from . import models

class AddOrganizationForm(forms.ModelForm):
    class Meta:
        model = models.Organization
        fields = [
            'province_name',
            'organization_name',
            'organization_phone_number',
            'workers_size',
            'manufacturedـproducts',
            'owner_full_name',
            'owner_phone_number',
            'owner_email',
            
        ]