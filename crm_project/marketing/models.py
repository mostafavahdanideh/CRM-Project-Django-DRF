from django.db import models
from django.core import validators
from django.db.models.expressions import F
from django.utils.translation import ugettext_lazy as _
from django_jalali.db import models as jmodels
from django.contrib.auth import get_user_model


min_length_validator = validators.MinValueValidator(
    limit_value=0, 
    message=("discount can't be negative"))


max_length_validator = validators.MaxValueValidator(
    limit_value=100, 
    message=("discount can't be more than 100"))


class Quote(models.Model):

    owner = models.ForeignKey(
        "organization.Organization",
        on_delete=models.PROTECT,
        verbose_name=_("سازمان"))
    
    creator = models.ForeignKey(
        get_user_model(),
        verbose_name=_("کارشناس ایجاد کننده"),
        on_delete=models.PROTECT,
        default=None
    )

    created_time = jmodels.jDateTimeField(
        auto_now_add=True,
        verbose_name=_("تاریخ ایجاد پیش فاکتور"))

    def __str__(self):
        return self.owner.organization_name
    
    def sum_all_base_cost(self):
        return self.quoteitem_set.aggregate(models.Sum('base_cost')).get('base_cost__sum', 0)
    
    def sum_final_cost(self):
        return self.quoteitem_set.aggregate(models.Sum('final_cost_with_discount')).get('final_cost_with_discount__sum', 0)


class QuoteItem(models.Model):

    quote = models.ForeignKey(
        "Quote",
        on_delete=models.CASCADE)

    product = models.ForeignKey(
        'inventory.CompanyProduct',
        on_delete=models.PROTECT
    )

    discount = models.FloatField(
        default=0.0,
        verbose_name=_("درصد تخفیف"),
        validators=[
            min_length_validator, 
            max_length_validator
            ]
    )

    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name=_("تعداد خرید")
    )

    base_cost = models.PositiveIntegerField(
        default=0,
        verbose_name=_("قیمت خام")
    )

    cost_with_taxation = models.PositiveIntegerField(
        default=0,
        verbose_name=_("قیمت با مالیات")
    )

    final_cost_with_discount = models.PositiveIntegerField(
        default=0,
        verbose_name=_("قیمت نهایی با تخفیف")
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
