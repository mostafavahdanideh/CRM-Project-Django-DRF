from django.contrib import messages
from django.http.response import Http404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import mixins
from . import models, forms
from organization import models as organization_models
from django.conf import settings
import os


class AddCompanyProduct(mixins.LoginRequiredMixin, generic.CreateView):
    form_class = forms.CompanyProductForm
    template_name = 'add_company_products.html'
    model = models.CompanyProduct
    success_url = reverse_lazy("inventory:list-company-products")

    def get(self, request, *args: str, **kwargs):
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        raise Http404
    
    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().post(request, *args, **kwargs)
        raise Http404

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
    paginate_by = 8

    def get(self, request, *args: str, **kwargs):
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        raise Http404


class DetailCompanyProduct(mixins.LoginRequiredMixin, generic.DetailView):
    template_name = 'detail_company_products.html'
    model = models.CompanyProduct

    def get(self, request, *args: str, **kwargs):
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        raise Http404


class UpdateCompanyProduct(mixins.LoginRequiredMixin, generic.UpdateView):
    template_name = "update_company_product.html"
    model = models.CompanyProduct
    form_class = forms.CompanyProductForm
    success_url = reverse_lazy("inventory:list-company-products")

    def get(self, request, *args: str, **kwargs):
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        raise Http404
    
    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().post(request, *args, **kwargs)
        raise Http404

    def form_valid(self, form):
        company_obj = self.get_object()
        image_catalog_path, pdf_catalog_path = None, None

        if company_obj.image_catalog and hasattr(company_obj.image_catalog, 'path'):
            image_catalog_path = os.path.join(settings.BASE_DIR, company_obj.image_catalog.path)
        
        if company_obj.pdf_catalog and hasattr(company_obj.pdf_catalog, 'path'):
            pdf_catalog_path = os.path.join(settings.BASE_DIR, company_obj.pdf_catalog.path)

        if "image_catalog" in form.files.keys() and image_catalog_path:
            os.remove(image_catalog_path)
        
        if "pdf_catalog" in form.files.keys() and pdf_catalog_path:
            os.remove(pdf_catalog_path)
        
        return super().form_valid(form)
