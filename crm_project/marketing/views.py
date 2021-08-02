from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import mixins
from django.core.mail import send_mail
from django.views import generic
from . import models, forms, tasks
from organization import models as org_models
import weasyprint


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
    model = models.QuoteItem
    form_class = forms.AddQuoteItemsForm

    def form_invalid(self, form):
        messages.info(self.request, form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organizations'] = org_models.Organization.objects.all()
        return context


class ListQuotes(mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'quotes_list.html'
    model = models.Quote
    paginate_by = 3

    def get_queryset(self):
        qs = super().get_queryset()

        if not self.request.user.is_superuser:
            qs = qs.filter(owner__expert_creator=self.request.user)

        return qs


class DetailQuotes(mixins.LoginRequiredMixin, generic.DetailView):
    template_name = 'detail_quote.html'
    model = models.Quote

    def quotes_for_user_exists(self):
        qs =  self.get_queryset()
        exists = qs.filter(owner__expert_creator=self.request.user).filter(pk=self.kwargs.get('pk', None)).exists()
        return exists

    def get(self, request, *args, **kwargs):
        if self.quotes_for_user_exists() or self.request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        else:
            return redirect("marketing:list_quotes")


class DownloadDetailQuote(mixins.LoginRequiredMixin, generic.DetailView):
    template_name = 'generate_quote_pdf.html'
    model = models.Quote

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        content = response.rendered_content
        pdf = weasyprint.HTML(string=content, base_url='http://127.0.0.1:8000').write_pdf()
        pdf_response = HttpResponse(content=pdf, content_type='application/pdf')
        return pdf_response


def send_quote_email(request):
    tasks.send_email_task.delay()
    return HttpResponse("Done!")
