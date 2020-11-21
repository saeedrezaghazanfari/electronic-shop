from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView
from .models import Product, Category, ProductVeiw, Favorites, ProductBrand, ProductColor, Chart
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Eshop_Order.forms import OrderForm

class Product_List_Page(ListView):
    template_name = 'Product_list.html'
    paginate_by = 9
    def get_queryset(self):
        return Product.objects.get_active_products()

class search_Product_nameBrandTag(ListView):
    template_name = 'Product_list.html'
    paginate_by = 9
    def get_queryset(self):
        request = self.request
        kww = request.GET.get('field')
        if kww is not None:
            return Product.objects.search_NameBrandTag(field=kww)
        return Product.objects.get_active_products()

def Product_Details_Page(request, *args, **kwargs):
    productID= kwargs.get('Product_ID')
    context = {
        'product': None,
        'tags': None,
        'related': None,
        'galleries': None,
        'view': 0,
        'shortlink': request.path,
        'productColors': None,
        'orderForm':None,
        'ex_fav': False,
        'times': None,
        'prices': None
    }
    product_selected: Product = Product.objects.get_by_id(product_id=productID)
    context['product'] = product_selected

    # Tags
    products_tags = product_selected.tag_set.all()
    context['tags'] = products_tags

    # Order
    orderForm = OrderForm(request.POST or None, initial={'productId': productID})
    context['orderForm'] = orderForm

    # Chart
    chartEX = Chart.objects.filter(product_id=productID, price=product_selected.price).first()
    if not chartEX:
        Chart.objects.create(product_id=productID, price=product_selected.price)
    context['prices'] = Chart.objects.filter(product_id=productID).values_list('price', flat=True).all()
    context['times'] = Chart.objects.filter(product_id=productID).values_list('timeStamp', flat=True).all()

    # relation Products
    category_name = product_selected.categories.first()
    related = Product.objects.filter(categories__title__iexact=category_name)
    context['related'] = related

    # Gallery
    galleries = product_selected.productgallery_set.all()
    context['galleries'] = galleries

    # Product Color
    productColors = ProductColor.objects.filter(product_id=productID, active=True).all()
    context['productColors'] = productColors

    # ex_favariots
    if request.user.is_authenticated:
        if Favorites.objects.filter(user_id=request.user.id, product_id=productID).first():
            context['ex_fav'] = True
        else:
            context['ex_fav'] = False
    else:
        context['ex_fav'] = False

    # View Product Counter
    if request.user.is_authenticated:
        thisUser = request.user
        if ProductVeiw.objects.filter(user_id=thisUser.id, product_id=productID).first() is None:
            ProductVeiw.objects.create(user_id=thisUser.id, product_id=productID)
    product_selected.views = ProductVeiw.objects.filter(product_id=product_selected.id).count()
    product_selected.save()
    a = ProductVeiw.objects.filter(product_id=productID).count()
    context['view'] = a

    return render(request, 'Product_Details.html', context)

def category_partial(request):
    categories: Category = Category.objects.all()
    context = {
        'categories': categories,
    }
    return  render(request, 'Category_partial.html', context)

def brand_partial(request):
    products: Product = Product.objects.all()
    ProductBrand.objects.all().delete()
    for product in products:
        ProductBrand.objects.create(productId=product.id, productBrand=product.brand, productName=product.title)

    brands = ProductBrand.objects.values_list('productBrand', flat=True).distinct()

    context = {
        'brands': brands,
    }
    return  render(request, 'Brands_product_partial.html', context)

@login_required(login_url='/Auth/Login')
def add_favorites(request):
    if request.is_ajax():
        productId = request.GET.get('productID')
        selected: Product = Product.objects.get(id=productId)
        thisUser = request.user
        isEx = Favorites.objects.filter(product_id=productId, user_id=thisUser.id).first()

        if isEx is None:
            selected.favorites_set.create(user_id=thisUser.id)
            return JsonResponse({'set': True})
        else:
            return JsonResponse({'set': False})

class Search_Category(ListView):
    template_name = 'Product_list.html'
    paginate_by = 9
    def get_queryset(self):
        kw = self.kwargs.get('product_category')
        return Product.objects.search_category(category=kw)

class Search_Brands(ListView):
    template_name = 'Product_list.html'
    paginate_by = 9
    def get_queryset(self):
        kw = self.kwargs.get('product_brand')
        return Product.objects.search_Brands(brand=kw)

def Search_Price(request):
    radioSelect = request.GET.get('filterProduct')
    get_price = request.GET.get('filterPrice')
    context = {
        'page_obj': None
    }

    if request.GET:
        if radioSelect == 'all':
            all_Products = Product.objects.filter(active=True)
            messages.info(request, f'تمامی محصولات در حال نمایش هستند !!')
            context['page_obj'] = all_Products
        elif radioSelect == 'price':
            founded = Product.objects.filter(price__lt=get_price)
            if founded:
                messages.info(request, f'محصولات با قیمت کمتر از <span class="number">{get_price}</span> تومان پیدا شدند.')
                context['page_obj'] = founded
            elif not founded:
                messages.info(request, f'محصولی در این محدوده قیمت پیدا نشد ، دوباره امتحان کنید!!')

    return render(request, 'Product_list.html', context)