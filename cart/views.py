from django.shortcuts import get_object_or_404, redirect, render

from courses.models import Course

from .cart import Cart

from django.contrib import messages

from .forms import CouponForm


def cart_detail(request):
    cart = Cart(request)
    form = CouponForm(request.POST or None)
    coupon = None
    cart_total_price = cart.get_total_price()
    if request.method == 'POST':
        if form.is_valid():
            code = form.cleaned_data['code']
            from .models import Coupon
            try:
                coupon = Coupon.objects.get(code__iexact=code)
                if coupon.is_valid():
                    price_after_discount = coupon.apply_coupon(cart_total_price)
                    messages.success(request, f'Coupon applied!')
                    cart_total_price = price_after_discount
                else:
                    messages.error(request, 'Coupon code is not valid at this time.')
            except Coupon.DoesNotExist:
                messages.error(request, 'Coupon code does not exist.')
            
    context = {
        'cart' : cart,
        'cart_total' : cart_total_price,
        'coupon_form' : form,
        
    }
    return render(request, 'cart/cart_detail.html', context=context)


def cart_add(request, course_id):
    cart = Cart(request)
    course = get_object_or_404(Course, pk=course_id)
    quantity = int(request.GET.get('quantity', 1))
    override_quantity = request.GET.get('override_quantity', 'False') == True
    cart.add_to_cart(course, quantity, override_quantity)
    return redirect('cart:detail')


def cart_remove(request, course_id):
    cart = Cart(request)
    course = get_object_or_404(Course, pk=course_id)
    cart.remove_from_cart(course)
    return redirect('cart:detail')


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('accounts:home')
