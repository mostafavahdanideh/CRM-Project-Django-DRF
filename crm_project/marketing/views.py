from django.shortcuts import render
from django.views import generic
from . import models


class OrganizationFollowUpHistory(generic.ListView):
    template_name = 'follow_up_history.html'
    model = models.FollowUp

    def get_queryset(self):
        qs = super().get_queryset()

        if not self.request.user.is_superuser:
            pk = self.kwargs.get('pk', None)
            qs = qs.filter(expert_creator=self.request.user, pk=pk)

        return qs
