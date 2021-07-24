from django.contrib import admin
from . import models


@admin.register(models.OrganizationProduct)
class OrganizationProductAdmin(admin.ModelAdmin):

    list_display = [
        'pk',
        'name',
    ]


@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):

    list_display = [
        'pk',
        'province_name',
        'organization_name',
        'organization_phone_number',
        'workers_size',
        'client_full_name',
        'client_phone_number',
        'client_email',
        'created_time',
        'expert_creator',

    ]

    search_fields = (
        'province_name',
        'organization_name',
        'client_full_name',
        'expert_creator__username',
    )

    list_editable = [
        'client_email',
        'expert_creator',
        'organization_phone_number',
        'client_full_name',
    ]

    list_filter = (
        'province_name',
        'expert_creator',
    )
