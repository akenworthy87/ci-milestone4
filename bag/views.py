from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404
)
from django.contrib import messages

from products.models import ProductInfo, ProductStock


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = get_object_or_404(ProductInfo, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    variety = None
    if 'product_variety' in request.POST:
        variety = request.POST['product_variety']
    bag = request.session.get('bag', {})

    if variety:
        if item_id in list(bag.keys()):
            if variety in bag[item_id]['items_by_variety'].keys():
                bag[item_id]['items_by_variety'][variety] += quantity
                messages.success(request,
                                 (f'Updated variety {variety.upper()} '
                                  f'{product.name} quantity to '
                                  f'{bag[item_id]["items_by_variety"][variety]}'))
            else:
                bag[item_id]['items_by_variety'][variety] = quantity
                messages.success(request,
                                 (f'Added variety {variety.upper()} '
                                  f'{product.name} to your bag'))
        else:
            bag[item_id] = {'items_by_variety': {variety: quantity}}
            messages.success(request,
                             (f'Added variety {variety.upper()} '
                              f'{product.name} to your bag'))
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(request,
                             (f'Updated {product.name} '
                              f'quantity to {bag[item_id]}'))
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    product = get_object_or_404(ProductInfo, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    variety = None
    if 'product_variety' in request.POST:
        variety = request.POST['product_variety']
    bag = request.session.get('bag', {})

    if variety:
        if quantity > 0:
            bag[item_id]['items_by_variety'][variety] = quantity
            messages.success(request,
                             (f'Updated variety {variety.upper()} '
                              f'{product.name} quantity to '
                              f'{bag[item_id]["items_by_variety"][variety]}'))
        else:
            del bag[item_id]['items_by_variety'][variety]
            if not bag[item_id]['items_by_variety']:
                bag.pop(item_id)
            messages.success(request,
                             (f'Removed variety {variety.upper()} '
                              f'{product.name} from your bag'))
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request,
                             (f'Updated {product.name} '
                              f'quantity to {bag[item_id]}'))
        else:
            bag.pop(item_id)
            messages.success(request,
                             (f'Removed {product.name} '
                              f'from your bag'))

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""

    try:
        product = get_object_or_404(ProductInfo, pk=item_id)
        variety = None
        if 'product_variety' in request.POST:
            variety = request.POST['product_variety']
        bag = request.session.get('bag', {})

        if variety:
            del bag[item_id]['items_by_variety'][variety]
            if not bag[item_id]['items_by_variety']:
                bag.pop(item_id)
            messages.success(request,
                             (f'Removed variety {variety.upper()} '
                              f'{product.name} from your bag'))
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
