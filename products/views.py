from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Min
from django.db.models.functions import Lower

from .models import ProductInfo, ProductStock, Category


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = (ProductInfo.objects
                .filter(product_discontinued=False)
                .annotate(display_price=Min('productlines__price')))
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'price':
                sortkey = 'display_price'
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        # Filtering by Category
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        # Searching
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request,
                               ("You didn't enter any search criteria!"))
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(ProductInfo, pk=product_id)
    lines = (product.productlines
             .filter(variety_discontinued=False))

    context = {
        'product': product,
        'lines': lines,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def product_management(request):
    return redirect('/admin/products/')


@login_required
def add_product(request):
    return redirect('/admin/products/productinfo/add/')


@login_required
def edit_product(request, product_id):
    return redirect(f'/admin/products/productinfo/{product_id}/change/')


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(ProductInfo, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))


# Soft delete functions
@login_required
def discontinue_product(request, product_id):
    """ Discontinue a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(ProductInfo, pk=product_id)
    product.product_discontinued = True
    product.save()
    messages.success(request, 'Product discontinued!')
    return redirect(reverse('products'))


@login_required
def discontinue_line(request, line_id):
    """ Discontinue a stock line from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    line = get_object_or_404(ProductStock, pk=line_id)
    line.variety_discontinued = True
    line.save()
    messages.success(request, 'Line discontinued!')
    return redirect(reverse('products'))
