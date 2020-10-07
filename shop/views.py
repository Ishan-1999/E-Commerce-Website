from django.shortcuts import render
from django.http import HttpResponse
import json


# Create your views here.
from .models import Product, Contact, Order, OrderUpdate


def home(request):
    return render(request, "home.html")


def boys(request):
    products = Product.objects.filter(gender="M")
    params = {'products': products}
    return render(request, "boys.html", params)


def girls(request):
    products = Product.objects.filter(gender="F")
    params = {'products': products}
    return render(request, "girls.html", params)


def productView(request, myId):
    breadcrumb = ""
    # fetching product using id
    prods = Product.objects.filter(id=myId)
    if 'Boys' in request.POST:
        breadcrumb = 'Boys'
    elif 'Girls' in request.POST:
        breadcrumb = 'Girls'


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


def checkout(request,):
    if request.method == 'POST':
        items_json = request.POST.get('items_json', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        phone = request.POST.get('phone', '')
        zip_code = request.POST.get('zip_code', '')

        order = Order(items_json=items_json, name=name, email=email, address=address, city=city, state=state, phone=phone, zip_code=zip_code)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The Order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, "checkout.html", {'thank': thank,'id': id})

    return render(request, "checkout.html")


def tracker(request,):
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
                    response = json.dumps(updates)
                    return HttpResponse(response)
            else:
                pass
        except Exception as e:
            pass

    return render(request, "tracker.html", )