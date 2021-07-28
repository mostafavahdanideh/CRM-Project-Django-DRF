from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_jalali.db import models as jmodels
from django.contrib.auth import get_user_model


class Quote(models.Model):

    owner = models.ForeignKey(
        "organization.Organization",
        on_delete=models.PROTECT,
        verbose_name=_("سازمان"))

    created_time = jmodels.jDateTimeField(
        auto_now_add=True,
        verbose_name=_("تاریخ ایجاد پیش فاکتور"))

    def __str__(self):
        return self.owner.organization_name
    

class QuoteItem(models.Model):

	quote = models.ForeignKey(
        "Quote",
        on_delete=models.CASCADE)

	product = models.ForeignKey(
        'inventory.CompanyProduct',
        on_delete=models.PROTECT
    )

	quantity = models.PositiveIntegerField(
        default=1,
        verbose_name=_("تعداد خرید")
    )

	price = models.PositiveIntegerField(
        default=0,
        verbose_name=_("قیمت محصول")
    )

	discount = models.FloatField(
        default=0.0,
        verbose_name=_("تخفیف")
    )


class FollowUp(models.Model):

    organization = models.ForeignKey(
        'organization.Organization',
        verbose_name=_("سازمان"),
        on_delete=models.CASCADE
    )

    expert_creator = models.ForeignKey(
        get_user_model(),
        verbose_name=_("کارشناس ایجاد کننده"),
        on_delete=models.PROTECT
    )

    created_time = jmodels.jDateTimeField(
        auto_now_add=True,
        verbose_name=_("تاریخ ایجاد پیش فاکتور")
    )

    content = models.TextField(
        verbose_name=_('متن پیگیری'),
        max_length=400,
        default=None
    )


# class EmailHistory(models.Model):
#     pass
