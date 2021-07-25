from django.contrib import admin
from . import models


class QuoteItemInline(admin.TabularInline):
    model = models.QuoteItem
    fields = [
        'quote',
        'product',
        'quantity',
        'price',
        'discount'
    ]


@admin.register(models.Quote)
class QuoteAdminManagement(admin.ModelAdmin):
    inlines = (
        QuoteItemInline,
    )
