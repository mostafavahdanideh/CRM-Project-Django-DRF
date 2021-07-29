from django.http.response import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from . import forms, models
from inventory import models as inventory_models


class CreateOrganization(LoginRequiredMixin, generic.CreateView):
    model = models.Organization
    template_name = 'register.html'
    form_class = forms.AddOrganizationForm
    success_url = reverse_lazy("organization:list")

    def form_valid(self, form):
        form.instance.expert_creator = self.request.user
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.info(self.request, form.errors)
        return super().form_invalid(form)
    

class ListOrganization(LoginRequiredMixin, generic.ListView):
    model = models.Organization
    template_name = "organization_list.html"
    paginate_by = 3

    def get_queryset(self):
        qs = super().get_queryset()

        if not self.request.user.is_superuser:
            qs = qs.filter(expert_creator=self.request.user)
            
        return qs


class DetailOrganization(LoginRequiredMixin, generic.DetailView):
    template_name = 'organization_details.html'
    model = models.Organization

    def organization_for_user_exists(self):
        qs =  self.get_queryset()
        exists = qs.filter(expert_creator=self.request.user).filter(pk=self.kwargs.get('pk', None)).exists()
        return exists

    def get(self, request, *args, **kwargs):
        if self.organization_for_user_exists() or self.request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        else:
            return redirect("organization:list")
    
    def get_suggestion_products(self):
        organization_obj = self.get_object()
        manufacturedـproducts = organization_obj.manufacturedـproducts.all()
        unique_suggestion_products = inventory_models.CompanyProduct.objects.filter(related_with_manufacturedـproducts__in=manufacturedـproducts).distinct()
        return unique_suggestion_products

    def get_provinces(self, context):
        organization_object = context['object']
        qs_provinces = models.Province.objects.exclude(name=organization_object.province)
        return qs_provinces

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['provinces'] = self.get_provinces(context)
        context['suggestion_products'] = self.get_suggestion_products()
        return context


class UpdateOrganization(LoginRequiredMixin, generic.UpdateView):
    queryset = models.Organization.objects.all()
    fields = (
        'province',
        'organization_phone_number',
        'workers_size',
        'owner_phone_number',
        'owner_first_name',
        'owner_last_name',
        'owner_second_last_name',
        'owner_email',
    )

    def get_object(self, queryset=None):
        pk = self.request.GET.get("pk", None)
        if pk:
            if pk.isdigit():
                user = self.request.user
                organization_obj = get_object_or_404(klass=models.Organization, pk=pk)

                if (user == organization_obj.expert_creator) or (user.is_superuser):
                    return organization_obj
                else:
                    raise Http404
            else:
                raise Http404
        else:
            raise Http404
    
    def form_valid(self, form):
        form.save()

        return JsonResponse(
            {
                'messages': "You've successfully updated",
            }, status=200
        )
    
    def form_invalid(self, form):
        return JsonResponse(
            {
                'messages': form.errors,
            }, status=400
        )
