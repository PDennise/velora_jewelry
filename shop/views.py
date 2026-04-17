from django.views.generic import ListView, DetailView
from .models import Product, Category

# Create your views here.

class ProductListView(ListView):                # Get the table from DB and send it to template as a list
    paginate_by = 6                             # Enable pagination (6 products per page)
    model = Product
    template_name = "shop/product_list.html"    #template path
    context_object_name = "products"            # variable name in the template

    # Apply filters based on query parameters (category, type, search)
    def get_queryset(self):
        queryset = Product.objects.select_related("category").all()
        category_id = self.request.GET.get("category") # Makes category filter
        product_type = self.request.GET.get("type")
        search_query = self.request.GET.get("q")
        sort = self.request.GET.get("sort")

        if sort == "price_asc":
            queryset = queryset.order_by("price")
        elif sort == "price_desc":
            queryset = queryset.order_by("-price")

        if category_id:
            queryset = queryset.filter(category_id=category_id) 
        if product_type:
            queryset = queryset.filter(product_type=product_type)
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category = self.request.GET.get("category")

        context["categories"] = Category.objects.all() # Send to templates
        context["product_type_choices"] = Product.PRODUCT_TYPE_CHOICES
        context["selected_category"] = int(category) if category else None  # Convert category ID from string to int for template comparison
        context["selected_type"] = self.request.GET.get("type", "")
        context["search_query"] = self.request.GET.get("q", "")
        context["selected_sort"] = self.request.GET.get("sort", "")
        return context

class ProductDetailView(DetailView):            # Get one product by pk from DB and send it to the detail page
    model = Product
    template_name = "shop/product_detail.html"
    context_object_name = "product"