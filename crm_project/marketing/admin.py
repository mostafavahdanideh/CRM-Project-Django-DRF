from django.contrib import admin
from . import models


class QuoteItemInline(admin.TabularInline):

    model = models.QuoteItem
    fields = [
        'quote',
        'product',
        'product_price',
        'discount',
        'quantity',
        'base_cost',
        'cost_with_taxation',
        'final_cost_with_discount',
    ]


@admin.register(models.QuoteItem)
class QuoteItemsAdminManagement(admin.ModelAdmin):
    pass


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


@admin.register(models.QuoteFollowUp)
class FollowUpAdmin(admin.ModelAdmin):
    pass


@admin.register(models.QuoteEmailHistory)
class EmailHistoryAdmin(admin.ModelAdmin):

    list_display = [
        'pk',
        'receiver_email_address',
        'was_successfull',
        'created_time',
        'user_sender',
    ]

    ordering = [
        '-created_time',
    ]
