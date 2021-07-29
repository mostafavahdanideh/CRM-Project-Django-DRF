from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import mixins
from . import models, forms
from organization import models as organization_models


class AddCompanyProduct(mixins.LoginRequiredMixin, generic.CreateView):
    form_class = forms.AddCompanyProductForm
    template_name = 'add_company_products.html'
    model = models.CompanyProduct
    success_url = reverse_lazy("inventory:list-company-products")

    def form_invalid(self, form):
        messages.info(self.request, form.errors)
        return super().form_invalid(form)
    
    def get_all_manufactured_product(self):
        all_organization_products = organization_models.OrganizationProduct.objects.all()
        return all_organization_products
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_organization_products'] = self.get_all_manufactured_product()
        return context


class ListCompanyProduct(mixins.LoginRequiredMixin, generic.ListView):
    model = models.CompanyProduct
    template_name = 'list_company_products.html'
    paginate_by = 4
