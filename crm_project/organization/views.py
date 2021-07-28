from django.http.response import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from . import forms, models
from inventory import models as inventory_models


class CreateOrganization(generic.CreateView):
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
    

class ListOrganization(generic.ListView):
    model = models.Organization
    template_name = "organization_list.html"
    paginate_by = 3

    def get_queryset(self):
        qs = super().get_queryset()

        if not self.request.user.is_superuser:
            qs = qs.filter(expert_creator=self.request.user)
            
        return qs


class DetailOrganization(generic.DetailView):
    template_name = 'organization_details.html'
    model = models.Organization

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        organization_object = context['object']
        qs_province = models.Province.objects.exclude(name=organization_object.province)
        context['provinces'] = qs_province
        return context


class UpdateOrganization(generic.UpdateView):
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