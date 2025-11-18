from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse
from django.conf import settings
from django.utils.translation import gettext as _

from .models import PaymentTransaction
from courses.models import Course, Enrollment

from cart.cart import Cart

import requests
import json

CALLBACK_URL = "http://127.0.0.1:8000/payment/verify/" # آدرس واقعی سایت خود را قرار دهید

@login_required
def send_request(request):
    cart = Cart(request)
    amount_toman = cart.get_total_price()
    amount_rial = amount_toman * 10
    
    course_ids = list(cart.cart.keys())
    
    # 2. ایجاد تراکنش در دیتابیس
    transaction = PaymentTransaction.objects.create(
        user=request.user,
        course_slugs_json=json.dumps(course_ids), # ذخیره آیدی دوره‌ها به جای اسلاگ
        amount=amount_rial, 
    )
    ## For zarinpal
    req_headers = {
        'accept' : 'application/json',
        'content-type' : 'application/json',
    }
    
    req_data = {
        'merchant_id' : settings.ZARINPAL_MERCHANT_ID, 
        'amount' : amount_rial,
        'description' : f'خرید دوره',
        # 'callback_url' : CALLBACK_URL,
        'callback_url' : request.build_absolute_uri(reverse('payment:verify')),
    }
    
    ZARINPAL_REQUEST_URL = 'https://payment.zarinpal.com/pg/v4/payment/request.json'
    response = requests.post(url = ZARINPAL_REQUEST_URL, json = req_data, headers = req_headers)
    
    data = response.json()['data']
    authority = data['authority']
    PaymentTransaction.authority = authority
    PaymentTransaction.save()
    
    if 'errors' not in data and len(data['errors']) == 0:
        return redirect('https://payment.zarinpal.com/pg/StartPay/{authority}'.format(authority = authority))
    else:
        return HttpResponse(_('Error from zarinpal'))


@login_required
def verify_payment(request):
    authority = request.GET.get('Authority')
    status = request.GET.get('Status') # OK یا Empty
    
    
    if status == 'OK':
        # 1. پیدا کردن تراکنش در دیتابیس
        try:
            transaction = PaymentTransaction.objects.get(authority=authority, user=request.user, is_paid=False)
        except PaymentTransaction.DoesNotExist:
            return HttpResponse("تراکنش یافت نشد یا قبلاً پرداخت شده است.", status=404)
        
        # # 2. ارسال درخواست تأیید نهایی (Verify)
        # zarinpal = Zarinpal()
        # response = zarinpal.verify(
        #     MERCHANT_ID=ZARINPAL_MERCHANT_ID,
        #     Amount=transaction.amount,
        #     Authority=authority,
        # )
        req_headers = {
        'accept' : 'application/json',
        'content-type' : 'application/json',
        }
        
        req_data = {
        'merchant_id' : settings.ZARINPAL_MERCHANT_ID,
        'amount' : transaction.amount,
        'authority' : authority,
        }  
        
        ZARINPAL_VERIFY_URL = 'https://payment.zarinpal.com/pg/v4/payment/verify.json'
        response = requests.post(url = ZARINPAL_VERIFY_URL, json = req_data, headers = req_headers)
        
        # if response.json().get['data'] and ('errors' not in response.json()['data'] or len(response.json()['data']['errors']) == 0 ):
        if 'data' in response.json() and ('errors' not in response.json()['data'] or len(response.json()['data']['errors']) == 0 ):
            data = response.json()['data']
            payment_code = data['code']

            if payment_code == 100:
                
                # الف. به‌روزرسانی تراکنش
                transaction.is_paid = True
                transaction.ref_id = data['ref_id']
                transaction.save()
                
                course_ids = json.loads(transaction.course_slugs_json) # در اینجا آیدی‌ها ذخیره شده‌اند
                courses_to_enroll = Course.objects.filter(id__in=course_ids)
                for course in courses_to_enroll:
                # ثبت‌نام و به‌روزرسانی تعداد دانشجویان
                    Enrollment.objects.get_or_create(student=request.user, course=course)
                    course.number_of_students += 1
                    course.save()
                    
                cart = Cart(request)
                cart.clear()
                # ج. نمایش پیام موفقیت و ریدایرکت
                # شما می‌توانید یک صفحه موفقیت درست کنید یا مستقیماً به صفحه دوره بروید.
                return redirect('courses:my_courses') 
            else:
                # تأیید ناموفق (ممکن است پول از حساب کم شده باشد اما به حساب مقصد نرسیده باشد)
                # نمایش پیام خطا به کاربر و ارجاع به پشتیبانی
                return render(request, 'payment/failure.html', {
                    'message': "پرداخت ناموفق بود.",
                    'status_code': response.get('Status')
                })
        else:
            # کاربر از پرداخت انصراف داده است
            return render(request, 'payment/failure.html', {'message': "پرداخت لغو شد."})