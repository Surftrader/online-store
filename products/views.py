from django.shortcuts import render
from .models import Product, Category
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
