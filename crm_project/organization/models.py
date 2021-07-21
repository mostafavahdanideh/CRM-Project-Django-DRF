from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model


phone_regex = RegexValidator(
    regex='^0[0-9]{2,}[0-9]{7,}$', 
    message='phone number is invalid')


class OrganizationProduct(models.Model):

    name = models.CharField(
        verbose_name=_("نام محصول"),
        max_length=50)
    
    def __str__(self):
        return self.name


class Organization(models.Model):

    province_name = models.CharField(
        verbose_name=_('نام استان'),
        max_length=50)

    organization_name = models.CharField(
        verbose_name=_('نام سازمان'),
        max_length=50)

    organization_phone_number = models.CharField(
        verbose_name=_('شماره تلفن سازمان'), 
        validators=[phone_regex], 
        max_length=11)

    workers_number = models.PositiveIntegerField(
        verbose_name=_('تعداد کارگران'), 
        default=1)

    manufacturedـproducts = models.ManyToManyField(
        'OrganizationProduct', 
        verbose_name=_('محصولات تولیدی'))

    expert_full_name = models.CharField(
        verbose_name=_("نام خانوادگی مخاطب"),
        max_length=50)

    expert_phone_number = models.CharField(
        verbose_name=_('شماره تلفن مخاطب'), 
        validators=[phone_regex], 
        max_length=11)

    expert_email = models.EmailField(
        verbose_name=_('ایمیل'))

    created_time = models.DateTimeField(
        verbose_name=_('تاریخ ایجاد شده'), 
        auto_now_add=True)

    creator = models.ForeignKey(
        get_user_model(), 
        verbose_name=_('ایحاد کننده'), 
        on_delete=models.PROTECT)

    def __str__(self):
        return self.organization_name
