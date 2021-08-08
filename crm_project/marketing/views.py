from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth import mixins
from django.views import generic
from . import my_statics, forms, tasks, models as marketing_models
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

    def get_all_organizations(self):
        return organization_models.Organization.objects.all()
    
    def get_expert_creator_organizations(self):
        return organization_models.Organization.objects.filter(expert_creator=self.request.user)
    
    def get_none_quoteitems(self):
        return marketing_models.QuoteItem.objects.none()
    
    def get_organization_pk(self):
        return self.request.POST.get("organization_pk", None)

    def get_organization_obj(self):
        organization_pk = self.get_organization_pk()
        return organization_models.Organization.objects.get(pk=organization_pk)
    
    def create_quote(self):
        organization_obj = self.get_organization_obj()
        return marketing_models.Quote.objects.create(owner=organization_obj, creator=self.request.user)
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['forms_set'] = forms.AddQuoteItemsFormSet(queryset=self.get_none_quoteitems())
        return super().render_to_response(context)

    def get_context_data(self, **kwargs):
        context = {}

        if self.request.user.is_superuser:
            context['organizations'] = self.get_all_organizations()
        else:
            context['organizations'] = self.get_expert_creator_organizations()

        return context
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['forms_set'] = forms.AddQuoteItemsFormSet(data=self.request.POST)
        forms_set = context['forms_set']

        if forms_set.has_changed() and forms_set.is_valid():
            for form in forms_set:
                organization_pk = self.get_organization_pk()

                if organization_pk and organization_pk.isdigit():
                    my_statics.save_calculation_related_with_quoteitems_model_fields(
                        form, 
                        self.create_quote())
                else:
                    forms_set.errors.append({'organization': "organization field is required"})
                    return render(request, template_name='create_quotes.html', context=context)
        else:
            forms_set.errors.insert(0, {'form': "form is empty"})
            return render(request, template_name='create_quotes.html', context=context)

        return redirect("marketing:list_quotes")


class EditQuotes(mixins.LoginRequiredMixin, generic.UpdateView):
    template_name = 'edit_quotes.html'
    pk_url_kwarg = 'quote_pk'
    model = marketing_models.QuoteItem
    quote_pk = None
    organization_pk = None

    def get_queryset(self):
        return marketing_models.Quote.objects.all()
    
    def get_organization(self):
        self.organization_pk = self.kwargs.get('organization_pk', None)
        return organization_models.Organization.objects.filter(pk=self.organization_pk)
    
    def get_items_in_quote(self):
        self.quote_pk = self.kwargs.get('quote_pk', None)
        return marketing_models.QuoteItem.objects.filter(quote__pk=self.quote_pk)
    
    def get_quote(self):
        return marketing_models.Quote.objects.get(pk=self.quote_pk)
    
    def get_successfull_redirect_url(self):
        return reverse("marketing:detail_quote", kwargs={"pk":self.quote_pk})
    
    def item_exists_in_quote(self, pk):
        items_in_quote = self.get_items_in_quote()
        return items_in_quote.filter(pk=pk).exists()

    def get_context_data(self, **kwargs):
        context = {}

        if self.request.method == "GET":
            context['forms_set'] = forms.UpdateQuoteItemsFormSet(queryset=self.get_items_in_quote())

        elif self.request.method == "POST":
            context['forms_set'] = forms.UpdateQuoteItemsFormSet(data=self.request.POST)

        return context
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        forms_set = context['forms_set']

        if forms_set.is_valid():
            for form in forms_set:
                if form.has_changed():
                    if self.item_exists_in_quote(form.instance.pk):
                        my_statics.save_calculation_related_with_quoteitems_model_fields(form)
                    else:
                        quote = self.get_quote()
                        my_statics.save_calculation_related_with_quoteitems_model_fields(form, quote)
        else:
            return render(request, template_name='edit_quotes.html', context=context)
        
        return redirect(self.get_successfull_redirect_url())


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
