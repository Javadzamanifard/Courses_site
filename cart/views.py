from django.shortcuts import get_object_or_404, redirect, render

from courses.models import Course

from .cart import Cart


def cart_detail(request):
    cart = Cart(request)
    context = {
        'cart' : cart,
        'cart_total' : cart.get_total_price()
    }
    return render(request, 'cart/cart_detail.html', context=context)


def cart_add(request, course_id):
    cart = Cart(request)
    course = get_object_or_404(Course, pk=course_id)
    quantity = int(request.Get.get('quantity', 1))
    override_quantity = request.Get.get('override_quantity', 'False') == True
    cart.add_to_cart(course, quantity, override_quantity)
    return redirect('cart:detail')


def cart_remove(request, course_id):
    cart = Cart(request)
    course = get_object_or_404(Course, pk=course_id)
    cart.remove_from_cart(course)
    return redirect('cart:deatail')


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('accounts:home')
