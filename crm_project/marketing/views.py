from django.contrib import messages
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import mixins
from django.views import generic
from django.db import transaction
from . import forms, tasks, models as marketing_models
from organization import models as organization_models
from inventory import models as inventory_models
import weasyprint


class OrganizationFollowUpHistory(generic.ListView):
    template_name = 'follow_up_history.html'
    model = marketing_models.QuoteFollowUp

    def get_queryset(self):
        qs = super().get_queryset()

        if not self.request.user.is_superuser:
            pk = self.kwargs.get('pk', None)
            qs = qs.filter(expert_creator=self.request.user, pk=pk)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        organization_obj = get_object_or_404(klass=organization_models.Organization, pk=self.kwargs.get('pk', None))
        context['organization'] = organization_obj
        return context


class CreateQuotes(mixins.LoginRequiredMixin, generic.CreateView):
    template_name = 'create_quotes.html'
    model = marketing_models.QuoteItem

    def get_context_data(self, **kwargs):
        context = {}
        
        if self.request.user.is_superuser:
            context['organizations'] = organization_models.Organization.objects.all()
        else:
            context['organizations'] = organization_models.Organization.objects.filter(expert_creator=self.request.user)

        if self.request.POST:
            context['forms_set'] = forms.AddQuoteItemsFormSet(data=self.request.POST)
        else:
            context['forms_set'] = forms.AddQuoteItemsFormSet()

        return context
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        forms_set = context['forms_set']

        organization = organization_models.Organization.objects.get(pk=request.POST.get("organization_pk", None))
        quote = marketing_models.Quote.objects.create(owner=organization, creator=request.user)

        if forms_set.is_valid():
            try:
                for form in forms_set:
                    form.instance.quote = quote

                    base_cost = form.instance.product.price * form.instance.quantity
                    cost_with_taxation = ((base_cost * 9) / 100) + base_cost
                    discount_amount = (cost_with_taxation * form.instance.discount) / 100
                    final_cost_with_discount = cost_with_taxation - discount_amount

                    form.instance.base_cost = base_cost
                    form.instance.cost_with_taxation = cost_with_taxation
                    form.instance.final_cost_with_discount = final_cost_with_discount

                    form.save()
            except:
                return self.form_invalid()
        else:
            return self.form_invalid()
        return HttpResponse("<h1>ok</h1>")

    def form_invalid(self, form):
        messages.info(self.request, form.errors)
        return super().form_invalid(form)


class ListQuotes(mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'quotes_list.html'
    model = marketing_models.Quote
    paginate_by = 3

    def get_queryset(self):
        qs = super().get_queryset()

        if not self.request.user.is_superuser:
            qs = qs.filter(owner__expert_creator=self.request.user)

        return qs


class DetailQuotes(mixins.LoginRequiredMixin, generic.DetailView):
    template_name = 'detail_quote.html'
    model = marketing_models.Quote

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
    model = marketing_models.Quote

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        content = response.rendered_content
        pdf = weasyprint.HTML(string=content, base_url='http://127.0.0.1:8000').write_pdf()
        pdf_response = HttpResponse(content=pdf, content_type='application/pdf')
        return pdf_response


def send_quote_email(request):
    organization_pk = request.GET.get('pk', None)

    if organization_pk:
        if organization_pk.isdigit():
            user_pk = request.user.pk
            tasks.send_email_task.delay(organization_pk, user_pk)

            return JsonResponse(
                data={
                    'message': "درخواست شما ارسال شد"
                },
                status=200
            )
    
    return JsonResponse(
            data={
                'message': "ارسال درخواست شما با مشکل مواجه شد لطفا دوباره ایمیل را ارسال کنید"
            },
            status=422
        )
