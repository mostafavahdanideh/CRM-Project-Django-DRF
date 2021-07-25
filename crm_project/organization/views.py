from django.views import generic
from django.urls import reverse_lazy
from . import forms, models


class CreateOrganization(generic.CreateView):
    model = models.Organization
    template_name = 'register.html'
    form_class = forms.AddOrganizationForm
    success_url = reverse_lazy("organization:register")

    def form_valid(self, form):
        form.instance.expert_creator = self.request.user
        return super().form_valid(form)
    

class ListOrganization(generic.ListView):
    model = models.Organization
    template_name = "organization_list.html"

    def get_queryset(self):
        qs = super().get_queryset()

        if not self.request.user.is_superuser:
            qs = qs.filter(expert_creator=self.request.user)
            
        return qs
        