from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from math import ceil

from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Import Payu from Paywix
from paywix.payu import Payu
from django.http import JsonResponse


# Create your views here.
from .models import Product, Contact, Order, OrderUpdate

key = 'E3Pd3z5P'

def home(request):
    return render(request, "home.html")

query = ''


def search(request):
    global query
    if request.method == 'GET':
        query = request.GET.get('search')
        allProds = []
        catprods = Product.objects.values('category')
        cats = {item['category'] for item in catprods}
        for cat in cats:
            prodtemp = Product.objects.filter(category=cat)
            prods=[item for item in prodtemp if searchMatch(query, item)]
            if len(prods)!= 0:
                allProds.append(prods)
    if request.method == 'POST':
        priceFilter = request.POST.get('priceFilter')
        allProds = []
        catprods = Product.objects.values('category')
        cats = {item['category'] for item in catprods}
        if priceFilter == 'LTH':
            for cat in cats:
                prodtemp = Product.objects.filter(category=cat).order_by('price')
                prods=[item for item in prodtemp if searchMatch(query, item)]
                if len(prods)!= 0:
                    allProds.append(prods)
            params = {'allProds': allProds, "msg":"", 'priceFilter': priceFilter}
            return render(request, "search.html", params)
        elif priceFilter == 'HTL':
            for cat in cats:
                prodtemp = Product.objects.filter(category=cat).order_by('price').reverse()
                prods=[item for item in prodtemp if searchMatch(query, item)]
                if len(prods)!= 0:
                    allProds.append(prods)
            params = {'allProds': allProds, "msg":"", 'priceFilter': priceFilter}
            return render(request, "search.html", params)
    params = {'allProds': allProds, "msg":""}
    if len(allProds)==0 or len(query)<4:
        params={'msg':"No Results Found."}
    return render(request, 'search.html', params)  


def searchMatch(query, item):
    if query.lower() in item.product_name.lower() or query.lower() in item.category.lower() or query.lower() in item.brand.lower():
        return True
    else:
        return False


def thrift(request):
    if request.method == 'POST':
        priceFilter = request.POST.get('priceFilter')
        if priceFilter == 'LTH':
            products = Product.objects.filter(gender="M").order_by('price')
            params = {'products': products, 'priceFilter': priceFilter}
            return render(request, "thrift.html", params)
        elif priceFilter == 'HTL':
            products = Product.objects.filter(gender="M").order_by('price').reverse()
            params = {'products': products, 'priceFilter': priceFilter}
            return render(request, "thrift.html", params)
    products = Product.objects.filter(gender="M")
    params = {'products': products}
    return render(request, "thrift.html", params)


def diy(request):
    if request.method == 'POST':
        priceFilter = request.POST.get('priceFilter')
        if priceFilter == 'LTH':
            products = Product.objects.filter(gender="M").order_by('price')
            params = {'products': products, 'priceFilter': priceFilter}
            return render(request, "diy.html", params)
        elif priceFilter == 'HTL':
            products = Product.objects.filter(gender="M").order_by('price').reverse()
            params = {'products': products, 'priceFilter': priceFilter}
            return render(request, "diy.html", params)
    products = Product.objects.filter(gender="M")
    params = {'products': products}
    return render(request, "diy.html", params)


def local(request):
    if request.method == 'POST':
        priceFilter = request.POST.get('priceFilter')
        if priceFilter == 'LTH':
            products = Product.objects.filter(gender="M").order_by('price')
            params = {'products': products, 'priceFilter': priceFilter}
            return render(request, "local.html", params)
        elif priceFilter == 'HTL':
            products = Product.objects.filter(gender="M").order_by('price').reverse()
            params = {'products': products, 'priceFilter': priceFilter}
            return render(request, "local.html", params)
    products = Product.objects.filter(gender="M")
    params = {'products': products}
    return render(request, "local.html", params)


def fnd(request):
    if request.method == 'POST':
        priceFilter = request.POST.get('priceFilter')
        if priceFilter == 'LTH':
            products = Product.objects.filter(gender="F").order_by('price')
            params = {'products': products, 'priceFilter': priceFilter}
            return render(request, "fnd.html", params)
        elif priceFilter == 'HTL':
            products = Product.objects.filter(gender="F").order_by('price').reverse()
            params = {'products': products, 'priceFilter': priceFilter}
            return render(request, "fnd.html", params)
    products = Product.objects.filter(gender="F")
    params = {'products': products}
    return render(request, "fnd.html", params)


def productView(request, myId):
    breadcrumb = ""
    # fetching product using id
    prods = Product.objects.filter(id=myId)
    if 'Thrift' in request.POST:
        breadcrumb = 'Thrift Store'
    elif 'diy' in request.POST:
        breadcrumb = 'DIY'
    elif 'local' in request.POST:
        breadcrumb = 'Local Sellers'
    elif 'fnd' in request.POST:
        breadcrumb = 'Foods & Drinks'


    return render(request, 'product.html', {'product': prods[0], 'bVal': breadcrumb})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()

    return render(request, "contact.html")


def cartview(request,):

    return render(request, "cartview.html", )


payu_config = settings.PAYU_CONFIG
merchant_key = payu_config.get('merchant_key')
merchant_salt = payu_config.get('merchant_salt')
surl = payu_config.get('success_url')
furl = payu_config.get('failure_url')
mode = payu_config.get('mode')

# Create Payu Object for making transaction
# The given arguments are mandatory
payu = Payu(merchant_key, merchant_salt, surl, furl, mode)

@csrf_exempt
@login_required
def checkout(request,):
    if request.method == 'POST':
        items_json = request.POST.get('items_json', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        phone = request.POST.get('phone', '')
        zip_code = request.POST.get('zip_code', '')

        order = Order(items_json=items_json, name=name, email=email, amount=amount, address=address, city=city, state=state, phone=phone, zip_code=zip_code)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The Order has been placed")
        update.save()
        thank = True
        id = order.order_id
        #request payu to transfer the amount to yours
        data = { 'amount': amount, 
             'firstname': name, 
             'email': email,
             'phone': phone,
             'productinfo': items_json, 
             'address1': address, 
             'city': city, 
             'state': state, 
             'zipcode': zip_code, 
             'udf1': '', 'udf2': '', 'udf3': '', 'udf4': '', 'udf5': ''
        }
        data.update({"txnid": id})
        payu_data = payu.transaction(**data)
        return render(request, 'payu_checkout.html', {"posted": payu_data, 'thank': thank})

    return render(request, "checkout.html")


def tracker(request):
    if request.method == 'POST':
        orderid = request.POST.get('orderid', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderid, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderid)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps(updates, default=str)
                    print(response)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')
    return render(request, "tracker.html", )

@csrf_exempt
def handlerequest(request):
    #paytm will send you post rqst
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print("order successful")
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'paymentstatus.html', {'response': response_dict})


# Payu success return page
@csrf_exempt
def payu_success(request):
    data = {k: v[0] for k, v in dict(request.POST).items()}
    data.update({'thank': True})
    return render(request, 'success.html', data)


# Payu failure page
@csrf_exempt
def payu_failure(request):
    data = {k: v[0] for k, v in dict(request.POST).items()}
    data.update({'thank': False})
    return render(request, 'failure.html', data)