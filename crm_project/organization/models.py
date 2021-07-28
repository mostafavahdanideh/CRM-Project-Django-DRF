from typing import Tuple
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from django_jalali.db import models as jmodels


owner_phone_number_regex = RegexValidator(
    regex='^(\+98|0)?9\d{9}$', 
    message="owner's phone number is invalid")

organization_phone_number_regext = RegexValidator(
    regex="^(\+98|0)?\d{1,2}\d{1,8}$",
    message="organization's phone number is invalid"
)


class OrganizationProduct(models.Model):

    name = models.CharField(
        verbose_name=_("نام محصول"),
        max_length=50)
    
    def __str__(self):
        return self.name


class Province(models.Model):
    name = models.CharField(
        verbose_name=_("استان"),
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.name


class Organization(models.Model):
    
    province = models.ForeignKey(
        'Province',
        verbose_name=_('نام استان'),
        on_delete=models.PROTECT,
        default=None
    )

    organization_name = models.CharField(
        verbose_name=_('نام سازمان'),
        max_length=50,
        unique=True)

    organization_phone_number = models.CharField(
        verbose_name=_('شماره تلفن سازمان'), 
        validators=[organization_phone_number_regext], 
        max_length=11,
        unique=True)

    workers_size = models.PositiveIntegerField(
        verbose_name=_('تعداد کارگران'), 
        default=1)

    manufacturedـproducts = models.ManyToManyField(
        'OrganizationProduct', 
        verbose_name=_('محصولات تولیدی'))

    
    owner_first_name = models.CharField(
        verbose_name=_("نام مخاطب"),
        max_length=50,
        default=None
    )

    owner_last_name = models.CharField(
        verbose_name=_('نام خانوادگی مخاطب'),
        max_length=50,
        default=None
    )

    owner_second_last_name = models.CharField(
        verbose_name=_('پسوند مخاطب'),
        max_length=50,
        blank=True,
        default=None
    )

    owner_phone_number = models.CharField(
        verbose_name=_('شماره تلفن مخاطب'), 
        validators=[owner_phone_number_regex], 
        max_length=11,
        unique=True
    )

    owner_email = models.EmailField(
        verbose_name=_('ایمیل مخاطب'),
        blank=True
    )

    created_time = jmodels.jDateTimeField(
        verbose_name=_('تاریخ ایجاد شده'), 
        auto_now_add=True
    )

    expert_creator = models.ForeignKey(
        get_user_model(), 
        verbose_name=_('کارشناس ایجاد کننده'), 
        on_delete=models.PROTECT
    )

    def __str__(self):
        return self.organization_name
