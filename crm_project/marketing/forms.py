from . import models
from django.forms import modelformset_factory
from django import forms


AddQuoteItemsFormSet = modelformset_factory(
    models.QuoteItem,
    fields = [
            'product',
            'quantity',
            'discount',
        ],
    extra=1
    )

UpdateQuoteItemsFormSet = modelformset_factory(
    models.QuoteItem,
    fields = [
            'product',
            'quantity',
            'discount',
        ],
    extra=0
    )


class CreateFollowUp(forms.ModelForm):
    class Meta:
        model = models.QuoteFollowUp
        fields = [
            'content'
        ]
