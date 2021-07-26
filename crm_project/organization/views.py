from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from . import forms, models


class CreateOrganization(generic.CreateView):
    model = models.Organization
    template_name = 'register.html'
    form_class = forms.AddOrganizationForm
    success_url = reverse_lazy("organization:register")

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
