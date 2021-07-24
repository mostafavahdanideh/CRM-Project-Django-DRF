from django.contrib import admin
from . import models


@admin.register(models.CompanyProduct)
class CompanyProductAdmin(admin.ModelAdmin):

    list_display = [
        'pk',
        'name',
        'has_taxation',
        'price',
        'technical_features',
    ]

    list_filter = (
        'has_taxation',
    )

    search_fields = (
        'name',
        'price',
    )

    ordering = (
        '-price',
        'name',
        )
    
    list_editable = [
        'has_taxation',
        'price',
    ]
