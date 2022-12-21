from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, reverse
from django.http import HttpResponse
from .models import Category, Product, Client, Order
from .forms import OrderForm, InterestForm, ClientForm, PasswordResetForm
# lab8-Import necessary classes and models
from django.contrib.auth import authenticate, login, logout, hashers
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime
import random
import string


# Create your views here.
def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    response = HttpResponse()
    heading1 = '<p>' + 'List of categories: ' + '</p>'
    response.write(heading1)
    for category in cat_list:
        para = '<p>' + str(category.id) + ': ' + str(category) + '</p>'
        response.write(para)

    # Update the index view function, so it displays a list of up to 5 Products as well. The Products should
    # be sorted in descending order of price (i.e. most expensive first).
    prod_list = Product.objects.all().order_by('-price')[:5]
    heading2 = '<p>' + 'List of products: ' + '</p>'
    response.write(heading2)
    for product in prod_list:
        para = '<p>' + str(product.id) + ': ' + str(product) + '</p>'
        response.write(para)

    return response


# Task2
def about(request):
    response = HttpResponse()
    heading = '<p>' + 'This is an Online Store APP.' + '<p>'
    response.write(heading)

    return response


# Task3
def detail(request, cat_no):
    response = HttpResponse()
    category = get_object_or_404(Category, pk=cat_no)
    locationHeading = '<p>' + 'Warehouse Location: ' + category.warehouse + '<p>'
    response.write(locationHeading)
    products = Product.objects.filter(category=category)
    heading2 = '<p>' + 'List of products: ' + '</p>'
    response.write(heading2)
    for product in products:
        para = '<p>' + str(product.id) + ': ' + str(product) + '</p>'
        response.write(para)

    return response


# Lab 6 starts from here using new functions for it rather than updating the previous ones.

# 1. Created directory for all the templates
# 2. Created new_index in the views.py

# 3. Created new index0.html and connected it with the new_index function in views.py solved all the subquestion in
# this part for question 5 Updated the index function such that clikcing on the category will foward you to page of
# each category ith its products
def new_index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index0.html', {'cat_list': cat_list})


# 4. Created new about0.html and connected it with new_about functiuon in views.py
# solved all the sub question in this part
def new_about(request):
    # Yes. created a new context variable
    heading = 'This is an online store app of U windsor'
    # passing the varibale created in the about part to the render function
    return render(request, 'myapp/about0.html', {'x': heading})


# 5. Created new detail0.html and connected it with new_detail function in views.py
# solved all the subquestion in this part
def new_detail(request, cat_no):
    category = get_object_or_404(Category, pk=cat_no)
    products = Product.objects.filter(category=category)
    return render(request, 'myapp/detail0.html', {'category': category, 'products': products})


# Lab 6 part2 starts from here and all the changes are stored in the new html files to understand the template inheritance.

# Used style.css from static folder and created new base.html for each of the below functions to help us learn the over ride in template inheritance

def part2_index(request):
    # cat_list = Category.objects.all().order_by('id')[:10]
    cat_list = Category.objects.all()
    if 'last_login' in request.session:
        last_login = request.session['last_login']
    else:
        last_login = 'Your last login was more than one hour ago'
    return render(request, 'myapp/index.html', {'cat_list': cat_list, 'last_login': last_login})


def part2_about(request):
    heading = 'This is an online store app of U windsor'
    if 'about_visits' in request.session:
        request.session['about_visits'] += 1
    else:
        request.session['about_visits'] = 1
        request.session.set_expiry(300)
    return render(request, 'myapp/about.html', {'x': heading, 'about_visits': request.session['about_visits']})


def part2_detail(request, cat_no):
    category = get_object_or_404(Category, pk=cat_no)
    products = Product.objects.filter(category=category)
    return render(request, 'myapp/detail.html', {'category': category, 'products': products})


# Lab 7 -->
def products(request):
    # prodlist = Product.objects.all().order_by('id')[:10]
    prodlist = Product.objects.all()
    return render(request, 'myapp/products.html', {'prodlist': prodlist})


def place_order(request):
    msg = ''
    prodlist = Product.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.num_units <= order.product.stock:
                order.save()
                # the function updates the stock field of the corresponding product
                order.product.stock -= order.num_units
                if order.product.stock == 0:
                    order.product.available = False
                order.product.save()
                msg = 'Your order has been placed successfully.'
            else:
                msg = 'We do not have sufficient stock to fill your order.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
        return render(request, 'myapp/place_order.html', {'form': form, 'msg': msg, 'prodlist': prodlist})


def productdetail(request, prod_id):
    product = get_object_or_404(Product, pk=prod_id)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["interested"] == "1":
                product.interested = product.interested + 1
                product.save()
                return redirect('/myapp/')
            else:
                return redirect('/myapp/')
        else:
            msg = 'There was an error in saving. Please try again'
            return render(request, 'myapp/interest_response.html', {'msg': msg})
    else:
        form = InterestForm()
        return render(request, 'myapp/productdetail.html', {'form': form, 'product': product})


# Lab 8
# generate the date and time of the current login. Store this value as a session 
def user_login(request):
    if request.user.is_authenticated:
        return redirect('myapp:part2_index')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                request.session['last_login'] = datetime.now().strftime("%B %d, %Y- %H:%M:%S")
                request.session.set_expiry(3600)
                if request.POST.get('next') != '':
                    return redirect(request.POST.get('next'))
                else:
                    return HttpResponseRedirect(reverse('myapp:part2_index'))
            else:
                # return HttpResponse('Your account is disabled.')
                return render(request, 'myapp/generic_response.html', {'response': 'Your account is disabled.'})
        else:
            # return HttpResponse('Invalid login details.')
            return render(request, 'myapp/generic_response.html', {'response': 'Invalid login details.'})
    else:
        return render(request, 'myapp/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:part2_index'))


# Feature4
def user_register(request):
    if request.user.is_authenticated:
        return redirect('myapp:part2_index')

    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES or None)
        if form.is_valid():
            client = form.save(commit=False)
            client.set_password(client.password)
            client.save()
            form.save_m2m()

            msg = 'Congratulations, You are now registered as a Client'
            return render(request, 'myapp/generic_response.html', {'response': msg})
    else:
        form = ClientForm()
    return render(request, 'myapp/register.html', {'form': form})


@login_required
def myorders(request):
    try:
        client = Client.objects.get(pk=request.user.id)
        orders = Order.objects.filter(client=client)
        return render(request, 'myapp/myorders.html', {'orders': orders, 'client': client})
    except Client.DoesNotExist:
        # return render(request, 'myapp/myorders.html')
        return render(request, 'myapp/generic_response.html', {'response': 'You are not a registered client!!'})


@login_required
def myprofile(request):
    try:
        client = Client.objects.get(pk=request.user.id)

        if request.method == 'POST':
            form = ClientForm(request.POST, request.FILES or None, instance=client)
            if form.is_valid() and form.has_changed():
                client = form.save(commit=False)
                if 'password' in form.changed_data:
                    client.set_password(client.password)
                client.save()
                form.save_m2m()

                msg = 'Your Client Profile is Updated'
                return render(request, 'myapp/generic_response.html', {'response': msg})
        else:
            form = ClientForm(instance=client)
            return render(request, 'myapp/myprofile.html', {'form': form, 'client': client})
    except Client.DoesNotExist:
        return render(request, 'myapp/generic_response.html', {'response': 'You are not a registered client!!'})


def reset_password(request):
    try:
        if request.method == 'POST':
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                thisClient = Client.objects.get(username=username)
                email = thisClient.email
                newPassword = ''.join(
                    random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
                encryptedPassword = hashers.make_password(newPassword)
                thisClient.password = encryptedPassword
                thisClient.save()
                message = "Your password has been changed successfully. Please find your new password: " + newPassword
                resetLink= "\nYou can change the password at: 127.0.0.1:8000/myapp/myprofile/"
                body = message+resetLink
                send_mail('Password changed successfully',
                          body,
                          settings.EMAIL_HOST_USER,
                          [email],
                          fail_silently=False)
                return render(request, 'myapp/reset_password.html', {'email': email})
        else:
            form = PasswordResetForm()
            return render(request, 'myapp/reset_password.html')

    except Client.DoesNotExist:
        return render(request, 'myapp/generic_response.html', {'response': 'You are not a registered client!!'})