from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import OrderCreateForm
from products.models import Product

@login_required
def order_create(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.product = product
            order.save()

            return render(request, 'orders/created.html', {'order': order})
    else:
 
        form = OrderCreateForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name
        })
    
    return render(request, 'orders/create.html', {
        'product': product,
        'form': form
    })
    