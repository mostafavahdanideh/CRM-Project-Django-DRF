from django.contrib import admin
from . import models


@admin.register(models.OrganizationProduct)
class OrganizationProductAdmin(admin.ModelAdmin):

    list_display = [
        'pk',
        'name',
    ]

    ordering = ['-pk']

    list_per_page = 7


@admin.register(models.Province)
class ProvinceAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):

    list_display = [
        'pk',
        'province',
        'organization_name',
        'organization_phone_number',
        'workers_size',
        'owner_first_name',
        'owner_last_name',
        'owner_second_last_name',
        'owner_phone_number',
        'owner_email',
        'created_on',
        'expert_creator',

    ]

    ordering = ['pk']

    search_fields = (
        'province',
        'organization_name',
        'owner_first_name',
        'owner_last_name',
        'owner_second_last_name',
        'expert_creator__username',
    )

    list_editable = [
        'province',
        'owner_email',
        'expert_creator',
        'organization_phone_number',
        'owner_phone_number',
        'owner_first_name',
        'owner_last_name',
        'owner_second_last_name',
    ]

    list_filter = (
        'province',
        'expert_creator',
    )

    list_per_page = 4

    @admin.display(description='format datatime')
    def created_on(self, obj):
        return obj.created_time.strftime("%Y/%m/%d  ,  %H:%M:%S")
