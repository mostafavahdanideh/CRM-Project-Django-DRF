

def save_calculation_related_with_quoteitems_model_fields(form, quote=None):
    quoteitems_obj = form.instance

    if quote:
        quoteitems_obj.quote = quote

    quoteitems_obj.base_cost = quoteitems_obj.calculating_base_cost()

    quoteitems_obj.cost_with_taxation = quoteitems_obj.calculating_cost_with_taxation(
        quoteitems_obj.base_cost)

    discount_amount = quoteitems_obj.calculating_discount_amount(
        quoteitems_obj.cost_with_taxation)

    quoteitems_obj.final_cost_with_discount = quoteitems_obj.calculating_final_cost_with_discount(
        quoteitems_obj.cost_with_taxation, 
        discount_amount)

    form.save()
