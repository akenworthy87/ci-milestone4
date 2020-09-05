from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import ProductInfo, ProductStock


def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})
    print(bag.items())
    for item_id, item_data in bag.items():
        if isinstance(item_data, int):
            print("Is Int")
            # product = get_object_or_404(ProductInfo, pk=item_id)
            # total += item_data * product.price
            # product_count += item_data
            # bag_items.append({
            #     'item_id': item_id,
            #     'quantity': item_data,
            #     'product': product,
            # })
        else:
            # product = get_object_or_404(ProductInfo, pk=item_id)
            for variety_id, quantity in item_data['items_by_variety'].items():
                line = get_object_or_404(ProductStock, pk=variety_id)
                total += quantity * line.price
                product_count += quantity
                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': line.product,
                    'variety': variety_id,
                    'line': line,
                })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
