from django.contrib import messages
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import mixins
from django.views import generic
from . import forms, tasks, models as marketing_models
from organization import models as organization_models
import weasyprint


class ListOrganizationFollowUpHistory(generic.ListView):
    template_name = 'follow_up_history.html'
    model = marketing_models.QuoteFollowUp
    paginate_by = 3

    def get_queryset(self):
        qs = super().get_queryset()
        pk = self.kwargs.get('pk', None)
        qs = qs.filter(organization__pk=pk)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        organization_obj = get_object_or_404(
            klass=organization_models.Organization, 
            pk=self.kwargs.get('pk', None))

        context['organization'] = organization_obj

        return context


class CreateOrganizationFollowUp(generic.CreateView):
    template_name = 'create_follow_up.html'
    model = marketing_models.QuoteFollowUp
    form_class = forms.CreateFollowUp

    def form_valid(self, form):
        form.instance.expert_creator = self.request.user

        form.instance.organization = get_object_or_404(
            klass=organization_models.Organization, 
            pk=self.kwargs.get('pk', None))

        form.save()

        return JsonResponse(
            data={
                'message': "your data successfully saved"
            }, status=200
        )
    
    def form_invalid(self, form):
        return JsonResponse(
            data={
                "errors": form.errors
            }, status=400)


class CreateQuotes(mixins.LoginRequiredMixin, generic.CreateView):
    template_name = 'create_quotes.html'
    model = marketing_models.QuoteItem

    def get_context_data(self, **kwargs):
        context = {}

        if self.request.method == "GET":

            if self.request.user.is_superuser:
                context['organizations'] = organization_models.Organization.objects.all()
            else:
                context['organizations'] = organization_models.Organization.objects.filter(
                    expert_creator=self.request.user)

            context['forms_set'] = forms.AddQuoteItemsFormSet(
                queryset=marketing_models.QuoteItem.objects.none())

        elif self.request.method == "POST":
            context['forms_set'] = forms.AddQuoteItemsFormSet(data=self.request.POST)

        return context
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        forms_set = context['forms_set']

        if forms_set.is_valid():
            try:
                organization = organization_models.Organization.objects.get(
                    pk=request.POST.get("organization_pk", None))

                quote = marketing_models.Quote.objects.create(
                    owner=organization, 
                    creator=request.user)

                for form in forms_set:
                    quoteitems_obj = form.instance

                    quoteitems_obj.quote = quote
                    quoteitems_obj.base_cost = quoteitems_obj.calculating_base_cost()
                    quoteitems_obj.cost_with_taxation = quoteitems_obj.calculating_cost_with_taxation(quoteitems_obj.base_cost)
                    discount_amount = quoteitems_obj.calculating_discount_amount(quoteitems_obj.cost_with_taxation)
                    quoteitems_obj.final_cost_with_discount = quoteitems_obj.calculating_final_cost_with_discount(
                        quoteitems_obj.cost_with_taxation, discount_amount)

                    form.save()
            except:
                messages.info(request, forms_set.errors)
        else:
            messages.info(request, forms_set.errors)

        return redirect("marketing:create_quote")


class EditQuotes(mixins.LoginRequiredMixin, generic.UpdateView):
    template_name = 'edit_quotes.html'
    model = marketing_models.Quote

    def get_context_data(self, **kwargs):
        context = {}

        if self.request.method == "GET":

            if self.request.user.is_superuser:
                context['organizations'] = organization_models.Organization.objects.all()
            else:
                context['organizations'] = organization_models.Organization.objects.filter(
                    expert_creator=self.request.user)

            context['forms_set'] = forms.AddQuoteItemsFormSet(
                queryset=marketing_models.QuoteItem.objects.filter(
                    quote__pk=self.kwargs.get('pk', None)))

        elif self.request.method == "POST":
            context['forms_set'] = forms.AddQuoteItemsFormSet(data=self.request.POST)

        return context


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

        exists = qs.filter(
            owner__expert_creator=self.request.user).filter(
                pk=self.kwargs.get('pk', None)).exists()

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
