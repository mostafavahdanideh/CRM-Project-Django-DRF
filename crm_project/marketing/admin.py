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

    list_display = [
        'owner',
        'created_on',
    ]

    @admin.display(description='format datatime')
    def created_on(self, obj):
        return obj.created_time.strftime("%Y/%m/%d  ,  %H:%M:%S")


@admin.register(models.FollowUp)
class FollowUpAdmin(admin.ModelAdmin):
    pass
