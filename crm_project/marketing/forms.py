from . import models
from django.forms import modelformset_factory


AddQuoteItemsFormSet = modelformset_factory(
    models.QuoteItem,
    fields = [
            'product',
            'quantity',
            'discount',
        ],
    extra=1
    )
