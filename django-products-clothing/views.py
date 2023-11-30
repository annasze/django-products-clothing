from django.db.models import Max
from django.views.generic import DetailView, ListView

from products import signals
from products.models import Product, Category, Color, SizeGroup
from products.filter import ProductFilter


class ProductList(ListView):
    model = Product
    filter = ProductFilter
    # do not display unavailable products on product list
    queryset = Product.prefetched.get_available_products()
    context_object_name = "products"
    paginate_by = 24
    ordering_param_name = "order_by"
    ordering_options = {
        "popularity": ["views"],
        "price_ascending": ["discounted_price", "price"],
        "price_descending": ["-discounted_price", "-price"],
        "newest": ["-pk"],
    }

    def get_queryset(self):
        q = self.get_Q_object()
        return self.queryset.filter(q)

    def get_Q_object(self):
        """
        Returns a django Q object for filtering
        based on query parameters
        """
        filters = {**self.request.GET}
        return ProductFilter(**filters).get_Q()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        # add data for filtering
        context['categories'] = Category.objects.filter(parent__isnull=True)
        context['colors'] = Color.objects.all()
        context['size_groups'] = SizeGroup.objects.all()
        context["max_price"] = self.queryset.aggregate(Max("price"))['price__max'] or 99999

        return context

    def get_ordering(self):
        ordering = self.request.GET.get(self.ordering_param_name) or ""

        return self.ordering_options.get(ordering, ["views"])


class ProductByCategoryList(ProductList):
    def get_queryset(self):
        # example path: dresses/summer-dresses/floral-dresses,
        # then crumb = "floral-dresses"
        crumb = self.kwargs["path"].split("/")[-1]
        ordering = super().get_ordering()
        q = self.get_Q_object()
        queryset = (
            Product.prefetched.get_queryset_for_category(crumb)
                .filter(q).order_by(*ordering)
        )

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        crumb = self.kwargs["path"].split("/")[0]
        context['categories'] = Category.objects.root_and_path_categories(crumb)
        return context


class ProductDetail(DetailView):
    model = Product
    # fetch all products, so that the user can see
    # an unavailable product as well (f.e. added to
    # bookmarks a week ago and currently out of stock)
    queryset = Product.prefetched.all()
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['other_products'] = self.queryset.filter(
            parent=self.get_object().parent
        )

        return context

    def get(self, request, *args, **kwargs):
        # send signal to increment views counter
        signals.product_viewed.send(
            sender=self.model,
            session=self.request.session,
            product=self.get_object(self.queryset),
        )
        return super().get(request, *args, **kwargs)
