from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import *
from .forms import *
from _decimal import Decimal

now = timezone.now()


@login_required
def index(request):
    return render(request, 'crm/home.html')


def sign_up(request):
    context = {}
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, 'crm/home.html')
        else:
            return render(request, 'registration/register.html', {'form': form})
    else:
        context['form'] = form
        return render(request, 'registration/register.html', context)


def home(request):
    return render(request, 'crm/home.html',
                  {'crm': home})


@login_required
def customer_list(request):
    customer = Customer.objects.filter(created_date__lte=timezone.now())
    return render(request, 'crm/customer_list.html',
                  {'customers': customer})


@login_required
@staff_member_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        # update
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.updated_date = timezone.now()
            customer.save()
            customer = Customer.objects.filter(created_date__lte=timezone.now())
            return render(request, 'crm/customer_list.html',
                          {'customers': customer})
    else:
        # edit
        form = CustomerForm(instance=customer)
    return render(request, 'crm/customer_edit.html', {'form': form})


@login_required
@staff_member_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    return redirect('crm:customer_list')


@login_required
def service_list(request):
    services = Service.objects.filter(created_date__lte=timezone.now())
    return render(request, 'crm/service_list.html', {'services': services})


@login_required
@staff_member_required()
def service_new(request):
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.created_date = timezone.now()
            service.save()
            services = Service.objects.filter(created_date__lte=timezone.now())
            return render(request, 'crm/service_list.html',
                          {'services': services})
    else:
        form = ServiceForm()
        # print("Else")
    return render(request, 'crm/service_new.html', {'form': form})


@login_required
@staff_member_required
def service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            service = form.save()
            # service.customer = service.id
            service.updated_date = timezone.now()
            service.save()
            services = Service.objects.filter(created_date__lte=timezone.now())
            return render(request, 'crm/service_list.html', {'services': services})
    else:
        # print("else")
        form = ServiceForm(instance=service)
    return render(request, 'crm/service_edit.html', {'form': form})


@login_required
@staff_member_required
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    service.delete()
    return redirect('crm:service_list')


@login_required
def product_list(request):
    products = Product.objects.filter(created_date__lte=timezone.now())
    return render(request, 'crm/product_list.html', {'products': products})


@login_required
@staff_member_required
def product_new(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_date = timezone.now()
            product.save()
            products = Product.objects.filter(created_date__lte=timezone.now())
            return render(request, 'crm/product_list.html',
                          {'products': products})
    else:
        form = ProductForm()
        # print("Else")
    return render(request, 'crm/product_new.html', {'form': form})


@login_required
@staff_member_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            # product.customer = product.id
            product.updated_date = timezone.now()
            product.save()
            products = Product.objects.filter(created_date__lte=timezone.now())
            return render(request, 'crm/product_list.html', {'products': products})
    else:
        # print("else")
        form = ProductForm(instance=product)
    return render(request, 'crm/product_edit.html', {'form': form})


@login_required
@staff_member_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('crm:product_list')


@login_required
@staff_member_required
def summary(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customers = Customer.objects.filter(created_date__lte=timezone.now())
    services = Service.objects.filter(cust_name=pk)
    products = Product.objects.filter(cust_name=pk)
    sum_service_charge = \
        Service.objects.filter(cust_name=pk).aggregate(Sum('service_charge'))
    sum_product_charge = \
        Product.objects.filter(cust_name=pk).aggregate(Sum('charge'))
    sum_product_service_charge = 0

    # if no product or service records exist for the customer,
    # change the ‘None’ returned by the query to 0.00
    sum = sum_product_charge.get("charge__sum")
    if sum == None:
        sum_product_charge = {'charge__sum': Decimal('0')}
    else:
        sum_product_service_charge = (sum_product_service_charge + sum)
    sum = sum_service_charge.get("service_charge__sum")
    if sum == None:
        sum_service_charge = {'service_charge__sum': Decimal('0')}
    else:
        sum_product_service_charge = (sum_product_service_charge + sum)

    return render(request, 'crm/summary.html', {'customer': customer, 'products': products, 'services': services,
                                                'sum_service_charge': sum_service_charge,
                                                'sum_product_charge': sum_product_charge,
                                                'sum_product_service_charge': sum_product_service_charge})
