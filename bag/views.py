from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404
)
from django.contrib import messages

from products.models import ProductStock


def view_bag(request):
    """ A view that renders the bag contents page """
    return render(request, 'bag/bag.html')


def add_to_bag(request):
    """ Add a quantity of the specified product to the shopping bag """

    line_id = request.POST['product_variety']
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')

    line = get_object_or_404(ProductStock, pk=line_id)
    bag = request.session.get('bag', {})

    # Checks product line isn't discontinued
    # This shouldn't be possible normally, but is a defensive check
    if line.variety_discontinued is True:
        messages.error(
            request,
            "Sorry, that product line is discontinued")
        return redirect(redirect_url)

    # Checks if quantity is greater than zero, rejects with error if not
    if quantity < 1:
        messages.error(
            request,
            "You can not add an item with zero quantity to the bag")
        return redirect(redirect_url)

    # First checks if line is already in the bag
    # Line in bag already; updates existing bag entry
    if line_id in list(bag.keys()):
        # Checks submitted quantity does not exceed stock availibilty
        if bag[line_id] + quantity > line.get_stock_avail():
            messages.error(
                request,
                "You can not add more stock than is availible.")
            return redirect(redirect_url)
        else:
            # Updates existing bag entry
            bag[line_id] += quantity
            messages.success(
                request,
                (f'Updated {line.variety_name.upper()} '
                    f'- {line.product.name} '
                    f'quantity to {bag[line_id]}'))
    # Line not in bag; adds line to bag
    else:
        # Checks submitted quantity does not exceed stock availibilty
        if quantity > line.get_stock_avail():
            messages.error(
                request,
                "You can not add more stock than is availible.")
            return redirect(redirect_url)
        else:
            # Adds line as new entry in bag
            bag[line_id] = quantity
            messages.success(
                request,
                (f'Added {line.variety_name.upper()} '
                    f'- {line.product.name} to your bag'))

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, line_id):
    """Adjust the quantity of the specified product to the specified amount"""

    line = get_object_or_404(ProductStock, pk=line_id)
    quantity = int(request.POST.get('quantity'))
    bag = request.session.get('bag', {})

    if quantity > 0:
        if quantity > line.get_stock_avail():
            messages.error(
                request,
                "You can not add more stock than is availible.")
            return redirect(reverse('view_bag'))
        bag[line_id] = quantity
        messages.success(
            request,
            (f'Updated {line.variety_name.upper()} '
                f'- {line.product.name} '
                f'quantity to {bag[line_id]}'))
    else:
        bag.pop(line_id)
        messages.success(
            request,
            (f'Removed {line.variety_name.upper()} '
                f'- {line.product.name} from your bag'))

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, line_id):
    """Remove the item from the shopping bag"""

    try:
        line = get_object_or_404(ProductStock, pk=line_id)
        bag = request.session.get('bag', {})

        bag.pop(line_id)
        messages.success(
            request,
            (f'Removed {line.variety_name.upper()} '
                f'- {line.product.name} from your bag'))

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
