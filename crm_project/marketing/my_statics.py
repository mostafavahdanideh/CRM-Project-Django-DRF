from . import models


def save_calculation_related_with_quoteitems_model_fields(form, quote=None):
    quoteitems_obj = form.instance

    # if the quote exist then we don't need to create new one (we use this condition when we want update quoteitems)
    if quote:
        quoteitems_obj.quote = quote

    # product_price has to be 0 and then we can set the current product price for our quote
    if not quoteitems_obj.product_price:
        quoteitems_obj.set_fixed_product_price()

    quoteitems_obj.base_cost = quoteitems_obj.calculating_base_cost()

    quoteitems_obj.cost_with_taxation = quoteitems_obj.calculating_cost_with_taxation(
        quoteitems_obj.base_cost)

    discount_amount = quoteitems_obj.calculating_discount_amount(
        quoteitems_obj.cost_with_taxation)

    quoteitems_obj.final_cost_with_discount = quoteitems_obj.calculating_final_cost_with_discount(
        quoteitems_obj.cost_with_taxation, 
        discount_amount)

    form.save()


def save_email_status_delivery(receiver_email, sender, was_successfull):
    models.QuoteEmailHistory.objects.create(
        receiver_email_address=receiver_email,
        was_successfull=was_successfull,
        user_sender=sender
    ).save()
