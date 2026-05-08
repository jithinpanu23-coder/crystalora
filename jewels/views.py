from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Product, Category

# Create your views here.
def home(request):
    return render(request, "home.html")
def about(request):
    return render(request, "about.html")
def contact(request):
    return render(request, "contact.html")

# FRONT PAGE (SHOW PRODUCTS)

def FRONT (request):

    category_id = request.GET.get('category')

    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()

    categories = Category.objects.all()

    return render(request, 'FRONT.html', {
        'products': products,
        'categories': categories
    })

def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('dashboard')

    return render(request, 'login.html')

@login_required
def dashboard(request):
    products = Product.objects.all()
    return render(request, 'dashboard.html', {'products': products})


@login_required
def add_product(request):
    if request.method == "POST":
        Product.objects.create(

            category_id=request.POST['category'],


            name=request.POST['name'],

            price=request.POST['price'],

            description=request.POST.get('description'),

            image=request.FILES['image']

        )
        return redirect('dashboard')

    return render(request, 'add_product.html')


@login_required
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        product.name = request.POST['name']
        product.price = request.POST['price']
        product.old_price = request.POST.get('old_price')
        product.description = request.POST.get('description')

        if request.FILES.get('image'):
            product.image = request.FILES['image']

        product.save()
        return redirect('dashboard')

    return render(request, 'edit_product.html', {'product': product})


@login_required
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('dashboard')