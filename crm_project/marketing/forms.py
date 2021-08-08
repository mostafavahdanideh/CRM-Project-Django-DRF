from . import models
from django.forms import modelformset_factory
from django import forms


QuoteItemsFormSet = modelformset_factory(
    models.QuoteItem,
    fields = [
            'product',
            'quantity',
            'discount',
        ],
    extra=1,
    can_delete=True
    )


class CreateFollowUp(forms.ModelForm):
    class Meta:
        model = models.QuoteFollowUp
        fields = [
            'content'
        ]
