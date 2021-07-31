from django.shortcuts import get_object_or_404, render
from django.contrib.auth import mixins
from django.views import generic
from . import models
from organization import models as org_models


class OrganizationFollowUpHistory(generic.ListView):
    template_name = 'follow_up_history.html'
    model = models.FollowUp

    def get_queryset(self):
        qs = super().get_queryset()

        if not self.request.user.is_superuser:
            pk = self.kwargs.get('pk', None)
            qs = qs.filter(expert_creator=self.request.user, pk=pk)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        organization_obj = get_object_or_404(klass=org_models.Organization, pk=self.kwargs.get('pk', None))
        context['organization'] = organization_obj
        return context



class CreateQuotes(mixins.LoginRequiredMixin, generic.CreateView):
    template_name = 'create_quotes.html'
    model = models.Quote


class ListQuotes(mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'quotes_list.html'
    model = models.Quote
