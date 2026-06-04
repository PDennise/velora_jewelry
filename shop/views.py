from django.views.generic import ListView, DetailView
from .models import Product, Category
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProductForm

# Create your views here.

class ProductListView(ListView):                # Get the table from DB and send it to template as a list
    paginate_by = 6                             # Enable pagination (6 products per page)
    model = Product
    template_name = "shop/product_list.html"    #template path
    context_object_name = "products"            # variable name in the template
    

    # Apply filters based on query parameters (category, type, search)
    # Separated filtering and sorting logic into modular methods for maintainability
    def get_queryset(self):
        queryset = Product.objects.select_related("category").all()

        # -------------------------
        # GET PARAMETERS
        # -------------------------

        params = self.request.GET
        category_slug = params.get("category")
        product_type = params.get("type")
        search_query = params.get("q", "").strip()
        sort = params.get("sort")
        bestseller = params.get("bestseller")

        # -------------------------
        # FILTERS
        # -------------------------

        if bestseller == "1":
            queryset = queryset.filter(featured=True)

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        if product_type:
            queryset = queryset.filter(product_type=product_type)

        if search_query:
            queryset = queryset.filter(
                Q(name__iexact=search_query) |
                Q(product_type__iexact=search_query)
            )

        # -------------------------
        # SORTING
        # -------------------------

        queryset = self.apply_sorting(queryset, sort)

        return queryset
    

    def apply_sorting(self, queryset, sort):
        sort_options = {
            "price_asc": "price",
            "price_desc": "-price",
            "newest": "-created_at",
        }

        return queryset.order_by(
            sort_options.get(sort, "-created_at")
        )
    
    def get_filter_query(self):
        params = self.request.GET.copy()
        params.pop("page", None)
        return params.urlencode()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        params = self.request.GET

        context.update({
            "categories": Category.objects.all(),
            "product_type_choices": Product.PRODUCT_TYPE_CHOICES,
            "selected_category": params.get("category") or "",
            "selected_type": params.get("type") or "",
            "search_query": params.get("q", ""),
            "selected_sort": params.get("sort", ""),
            "bestseller": params.get("bestseller", ""),

            # Banner
            "banner_image": "/static/assets/images/shop-jewelry-img.jpg",
            "title": "Shop Jewelry",
        })

        return context

class ProductDetailView(DetailView):            # Get one product from DB and send it to the detail page
    model = Product
    template_name = "shop/product_detail.html"
    context_object_name = "product"

    slug_field = "slug"
    slug_url_kwarg = "slug"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Banner
        context["banner_image"] = self.object.image.url

        return context



@staff_member_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()                           # Save the new product to the database
            messages.success(request, f'{product.name} successfully added.')
            return redirect('shop:product-detail', slug=product.slug)
    else:
        form = ProductForm()

    return render(
        request, 'shop/product_form.html',
        {
            'form': form,
            'action': 'Add',
            "banner_image": "/static/assets/images/shop-jewelry-img.jpg",
            "title": "Shop Jewelry",
        }
    )


@staff_member_required
def edit_product(request, slug):
    product = get_object_or_404(Product, slug=slug)        # Get the product or return 404

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()                           # Save the updated product
            messages.success(request, f'{product.name} successfully updated.')
            return redirect('shop:product-detail', slug=product.slug)
    else:
        form = ProductForm(instance=product)

    return render(request, 'shop/product_form.html', {'form': form, 'action': 'Edit', 'product': product})


@staff_member_required
def delete_product(request, slug):
    product = get_object_or_404(Product, slug=slug)        # Get the product or return 404

    if request.method == 'POST':
        product.delete()                                    # Delete the product from the database
        messages.success(request, 'Product successfully deleted.')
        return redirect('shop:product-list')

    return render(request, 'shop/product_confirm_delete.html', {'product': product})