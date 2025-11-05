from django.contrib import messages
from django.utils.translation import gettext as _

from courses.models import Course


class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart
    
    
    def add_to_cart(self, course, quantity = 1, override_quantity=False):
        course_id = str(course.id)
        if course_id not in self.cart:
            self.cart[course_id] = {'quantity': quantity, 'price' : course.price}
        else:
            messages.warning(self.request, _('This course already exists in your cart'))
        self.save()
    
    
    def save(self):
        self.session.modified = True
    
    
    def remove_from_cart(self, course):
        course_id = str(course.id)
        if course_id in self.cart:
            del self.cart[course_id]
        self.save()
    
    
    def clear(self):
        del self.session['cart']
        self.save()
    
    
    def __iter__(self):
        course_ids = self.cart.keys()
        courses = Course.objects.filter(id__in=course_ids)
        for course in courses:
            item = self.cart[str(course.id)]
            item['course'] = course
            item['price'] = course.price
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    
    def get_total_price(self):
        print("🧾 CART DATA:", self.cart)
        return sum(item['price'] * item['quantity'] for item in self.cart.values())