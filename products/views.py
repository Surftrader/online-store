from django.shortcuts import render, get_object_or_404
from .models import Product, Category, ViewedProduct
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
    # Get product by slug or return error 404
    product = get_object_or_404(Product, slug=slug, available=True)
    
    # Logics reviews:
    # If user is authenticated product will be saved to history
    if request.user.is_authenticated:
        # get_or_create prevents duplicates if the user refreshes the page
        ViewedProduct.objects.get_or_create(user=request.user, product=product)

    return render(request, 'products/detail.html', {
        'product': product
    })
    
    