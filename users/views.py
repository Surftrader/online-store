from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from .tasks import send_newsletter_email

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Автоматический вход после регистрации
            return redirect('products:product_list')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            send_newsletter_email.delay(email)
            messages.success(request, f'Дякуємо! Лист для {email} вже готується до відправлення.')
            return redirect(request.META.get('HTTP_REFERER', 'products:product_list'))
    return render(request, 'products/product_list')
