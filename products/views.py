from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, ViewedProduct
from reviews.forms import ReviewForm
from django.db.models import Q

def product_list(request):
    # Get parameters from URL (example, ?category=smartphones&search=iphone)
    category_slug = request.GET.get('category')
    search_query = request.GET.get('search')
    
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()

    # Filter by category (SQL: WHERE category_id = ...)
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    # Search (SQL: WHERE title ILIKE %...% OR description ILIKE %...%)
    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )

    return render(request, 'products/list.html', {
        'products': products,
        'categories': categories,
        'current_category': category_slug
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    
    # Processing the feedback form
    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('products:product_detail', slug=product.slug)
    else:
        form = ReviewForm()

    # Receive all reviews for this product
    reviews = product.reviews.all()

    # Logic of viewed products
    if request.user.is_authenticated:
        ViewedProduct.objects.get_or_create(user=request.user, product=product)

    return render(request, 'products/detail.html', {
        'product': product,
        'reviews': reviews,
        'review_form': form
    })    
    