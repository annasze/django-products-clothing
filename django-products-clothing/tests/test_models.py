from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Q
from django.test import TestCase

from products import models
from products.filter import ProductFilter


class Category:
    def __init__(self):
        self.category_dresses = None
        self.category_summer_dresses = None
        self.category_summer_dresses_mini = None
        self.category_trousers = None
        self.category_business_trousers = None

        self.set_categories()

    def set_categories(self):
        self.category_dresses = models.Category.objects.create(
            name='Dresses',
        )
        self.category_summer_dresses = models.Category.objects.create(
            name='Summer dresses',
            parent=self.category_dresses,
        )
        self.category_summer_dresses_mini = models.Category.objects.create(
            name='Mini dresses',
            parent=self.category_summer_dresses,
        )

        self.category_trousers = models.Category.objects.create(
            name='Trousers',
        )
        self.category_business_trousers = models.Category.objects.create(
            name='Business trousers',
            parent=self.category_trousers
        )


class Size:
    def __init__(self):
        self.size_group = None
        self.size_36 = None
        self.size_38 = None
        self.size_40 = None

        self.set_size_group()
        self.set_sizes()

    def set_size_group(self):
        self.size_group = models.SizeGroup.objects.create(
            name="Numerical"
        )

    def set_sizes(self):
        for size in ["40", "38", "36"]:
            obj = models.Size.objects.create(
                name=size,
                group=self.size_group
            )
            setattr(self, f"size_{size}", obj)


class Color:
    def __init__(self):
        self.color_red = None
        self.color_blue = None
        self.color_green = None

    def set_colors(self):
        self.color_red = models.Color.objects.create(
            name="red",
            hex_code="#ff0000"
        )
        self.color_green = models.Color.objects.create(
            name="green",
            hex_code="#00ff00"
        )
        self.color_blue = models.Color.objects.create(
            name="blue",
            hex_code="#0000ff"
        )


class ParentProduct(Category):
    def __init__(self):
        super(ParentProduct, self).__init__()
        self.linen_floral_dress = None
        self.sleeveless_dress = None
        self.business_trousers = None
        self.set_parent_products()

    def set_parent_products(self):
        self.linen_floral_dress = models.ParentProduct.objects.create(
            category=self.category_dresses,
            name="Linen floral dress"
        )
        self.sleeveless_dress = models.ParentProduct.objects.create(
            category=self.category_summer_dresses,
            name="Sleeveless dress"
        )
        self.business_trousers = models.ParentProduct.objects.create(
            category=self.category_business_trousers,
            name="Business trousers"
        )


class Product(ParentProduct, Size, Color):
    def __init__(self):
        super(Product, self).__init__()
        self.linen_floral_dress_cornflower = None
        self.linen_floral_dress_roses = None
        self.dress_with_invalid_disc_price = None
        self.sleeveless_dress_green = None
        self.business_trousers_navy_blue = None

        self.set_products()

    def set_products(self):
        self.linen_floral_dress_cornflower = models.Product.objects.create(
            parent=self.linen_floral_dress,
            style="Cornflower",
            color=self.color_blue,
            price=99,
            discounted_price=79,
            main_image_url="products/linen-floral-dress-cornflower.jpg"
        )
        self.linen_floral_dress_roses = models.Product.objects.create(
            parent=self.linen_floral_dress,
            style="Roses",
            color=self.color_red,
            price=109,
            discounted_price=69,
            main_image_url="products/linen-floral-dress-roses.jpg"
        )
        self.sleeveless_dress_green = models.Product.objects.create(
            parent=self.sleeveless_dress,
            style="Green",
            color=self.color_green,
            price=99,
            main_image_url="products/sleeveless-dress-green.jpg"
        )
        self.dress_with_invalid_disc_price = models.Product.objects.create(
            parent=self.sleeveless_dress,
            style="Red",
            color=self.color_red,
            price=79,
            discounted_price=99,
            main_image_url="products/sleeveless-dress-red.jpg"
        )
        self.business_trousers_navy_blue = models.Product.objects.create(
            parent=self.business_trousers,
            style="Navy blue",
            color=self.color_blue,
            price=199,
            main_image_url="products/business_trousers_nb.jpg"
        )


class Stock(Product):
    def __init__(self):
        super(Product, self).__init__()
        self.stock_linen_floral_dress_cornflower_36 = None
        self.stock_linen_floral_dress_cornflower_38 = None
        self.stock_linen_floral_dress_roses_36 = None
        self.stock_linen_floral_dress_roses_40 = None
        self.stock_business_trousers_navy_blue_36 = None
        self.stock_business_trousers_navy_blue_38 = None

        self.set_stocks()

    def set_stocks(self):
        self.stock_linen_floral_dress_cornflower_36 = models.Stock.objects.create(
            product=self.linen_floral_dress_cornflower,
            size=self.size_36,
            quantity=5
        )
        self.stock_linen_floral_dress_cornflower_38 = models.Stock.objects.create(
            product=self.linen_floral_dress_cornflower,
            size=self.size_38,
            quantity=0
        )
        self.stock_linen_floral_dress_roses_36 = models.Stock.objects.create(
            product=self.linen_floral_dress_roses,
            size=self.size_36,
            quantity=0
        )
        self.stock_linen_floral_dress_roses_40 = models.Stock.objects.create(
            product=self.linen_floral_dress_roses,
            size=self.size_40,
            quantity=0
        )
        self.stock_business_trousers_navy_blue_36 = models.Stock.objects.create(
            product=self.business_trousers_navy_blue,
            size=self.size_36,
            quantity=10
        )
        self.stock_business_trousers_navy_blue_38 = models.Stock.objects.create(
            product=self.business_trousers_navy_blue,
            size=self.size_38,
            quantity=0
        )


class CategoryTestCase(TestCase, Category):
    def setUp(self) -> None:
        self.set_categories()

    def test_path_crumb(self):
        self.assertEqual(self.category_dresses.path_crumb, 'dresses')
        self.assertEqual(self.category_summer_dresses.path_crumb, 'summer-dresses')

    def test_get_absolute_url(self):
        self.assertIn('dresses/', self.category_dresses.get_absolute_url())
        self.assertIn('dresses/summer-dresses/', self.category_summer_dresses.get_absolute_url())

    def test_str(self):
        self.assertEqual(str(self.category_dresses), 'Dresses')
        self.assertEqual(str(self.category_summer_dresses), 'Summer dresses')

    def test_root_and_path_categories_manager_method(self):
        categories = models.Category.objects.root_and_path_categories(crumb="summer-dresses")
        self.assertIn(self.category_dresses, categories)
        self.assertIn(self.category_summer_dresses, categories)
        self.assertIn(self.category_summer_dresses_mini, categories)
        self.assertIn(self.category_trousers, categories)
        self.assertNotIn(self.category_business_trousers, categories)

        categories = models.Category.objects.root_and_path_categories(crumb="trousers")
        self.assertIn(self.category_dresses, categories)
        self.assertNotIn(self.category_summer_dresses, categories)
        self.assertNotIn(self.category_summer_dresses_mini, categories)
        self.assertIn(self.category_trousers, categories)
        self.assertIn(self.category_business_trousers, categories)


class ColorTestCase(TestCase, Color):
    def setUp(self) -> None:
        self.set_colors()

    def test_str(self):
        self.assertEqual(str(self.color_blue), "blue")

    def test_correct_hex_code_is_set(self):
        orange = models.Color.objects.create(
            name="orange",
            hex_code="#ffa500"
        )
        orange.full_clean()
        orange.refresh_from_db()
        self.assertEqual(orange.hex_code, "#ffa500")

    def test_incorrect_hex_code_raises_error(self):
        orange = models.Color.objects.create(
            name="orange",
            hex_code="#fa500"
        )
        with self.assertRaises(ValidationError) as cm:
            orange.full_clean()
        self.assertIn(
            "'The provided hex_code: (%s) is invalid. "
            "Check the code and try again.'" % orange.hex_code,
            str(cm.exception)
        )


class SizeTestCase(TestCase, Size):
    def setUp(self) -> None:
        self.set_size_group()
        self.set_sizes()

    def test_str(self):
        self.assertEqual(str(self.size_group), "Numerical")
        self.assertEqual(str(self.size_36), "36")

    def test_sizes_ordering(self):
        sizes = ["40", "38", "36"]
        for i, size in enumerate(models.Size.objects.all()):
            self.assertEqual(size, getattr(self, f"size_{sizes[i]}"))


class ProductTestCase(TestCase, Product):
    def setUp(self) -> None:
        self.set_categories()
        self.set_colors()
        self.set_size_group()
        self.set_sizes()
        self.set_parent_products()
        self.set_products()

    def test_slug(self):
        self.assertEqual(self.linen_floral_dress_cornflower.slug, 'linen-floral-dress-cornflower')

    def test_str(self):
        self.assertEqual(str(self.linen_floral_dress_cornflower), "Linen floral dress - Cornflower")

    def test_name(self):
        self.assertEqual(self.linen_floral_dress_cornflower.name, "Linen floral dress - Cornflower")

    def test_get_absolute_url(self):
        self.assertIn("p/linen-floral-dress-cornflower/", self.linen_floral_dress_cornflower.get_absolute_url())

    def test_incorrect_discounted_price_raises_error(self):
        with self.assertRaises(ValidationError):
            self.dress_with_invalid_disc_price.full_clean()

    def test_parent_style_unique_constraint(self):
        with self.assertRaises(IntegrityError) as cm:
            models.Product.objects.create(
                parent=self.linen_floral_dress,
                style="cornflower",
                price=59,
                main_image_url="products/linen-cornflower.jpg"
            )
        self.assertIn("UNIQUE constraint failed", str(cm.exception))


class PrefetchedProductManagerTestCase(TestCase, Stock):
    def setUp(self) -> None:
        self.set_categories()
        self.set_colors()
        self.set_size_group()
        self.set_sizes()
        self.set_parent_products()
        self.set_products()
        self.set_stocks()

    def test_get_queryset(self):
        """
        Test that accessing attributes from the helper method
        requires exactly 4 database queries.
        """
        with self.assertNumQueries(4):
            products = models.Product.prefetched.get_queryset()

            for product in products:
                self.access_attributes(product)

    def test_get_available_products(self):
        products = models.Product.prefetched.get_available_products()
        with self.assertNumQueries(4):
            for product in products:
                self.access_attributes(product)
        self.assertIn(self.linen_floral_dress_cornflower, products)
        self.assertNotIn(self.linen_floral_dress_roses, products)
        self.assertEqual(products.count(), 2)

    def test_get(self):
        with self.assertNumQueries(4):
            product = models.Product.prefetched.get(style="Cornflower")
            self.access_attributes(product)

    def test_get_queryset_for_category_available_only(self):
        products = models.Product.prefetched.get_queryset_for_category(
            crumb="dresses"
        )
        with self.assertNumQueries(4):
            for product in products:
                self.access_attributes(product)

        self.assertIn(self.linen_floral_dress_cornflower, products)
        self.assertNotIn(self.linen_floral_dress_roses, products)

        products = models.Product.prefetched.get_queryset_for_category(
            crumb="trousers"
        )
        self.assertEqual(products.count(), 1)

    def test_get_queryset_for_category(self):
        products = models.Product.prefetched.get_queryset_for_category(
            crumb="dresses",
            available_only=False
        )
        self.assertIn(self.linen_floral_dress_cornflower, products)
        self.assertIn(self.linen_floral_dress_roses, products)

    @staticmethod
    def access_attributes(product):
        """
        A helper method which accesses the product attributes.
        """
        product.parent.description
        product.parent.fabric_info
        product.parent.sizes_info
        product.name
        product.style
        if product.color:
            product.color.name
            product.color.hex_code
        for size in product.sizes.all():
            size.name
        for stock in product.stock.all():
            stock.size.name
            stock.quantity
        for image in product.images.all():
            image.url


class ProductFilterTestCase(TestCase, Stock):
    def setUp(self) -> None:
        self.set_categories()
        self.set_colors()
        self.set_size_group()
        self.set_sizes()
        self.set_parent_products()
        self.set_products()
        self.set_stocks()
        self.qs = models.Product.objects.all()

    def test_price_gte_filter(self):
        f = ProductFilter(price_gte=["79"])
        filtered_qs = self.qs.filter(f.get_Q())
        self.assertIn(self.linen_floral_dress_cornflower, filtered_qs)
        self.assertNotIn(self.linen_floral_dress_roses, filtered_qs)
        self.assertIn(self.sleeveless_dress_green, filtered_qs)

    def test_price_lte_filter(self):
        f = ProductFilter(price_lte=["99"])
        filtered_qs = self.qs.filter(f.get_Q())
        self.assertIn(self.linen_floral_dress_cornflower, filtered_qs)
        self.assertIn(self.linen_floral_dress_roses, filtered_qs)
        self.assertIn(self.sleeveless_dress_green, filtered_qs)

    def test_disc_price_filter(self):
        f = ProductFilter(disc_price=["1"])
        filtered_qs = self.qs.filter(f.get_Q())
        self.assertIn(self.linen_floral_dress_cornflower, filtered_qs)
        self.assertIn(self.linen_floral_dress_roses, filtered_qs)
        self.assertNotIn(self.sleeveless_dress_green, filtered_qs)

    def test_color_filter(self):
        f = ProductFilter(color=['1', '2'])
        filtered_qs = self.qs.filter(f.get_Q())
        self.assertNotIn(self.linen_floral_dress_cornflower, filtered_qs)
        self.assertIn(self.linen_floral_dress_roses, filtered_qs)
        self.assertIn(self.sleeveless_dress_green, filtered_qs)

        f = ProductFilter(color=['1'])
        filtered_qs = self.qs.filter(f.get_Q())
        self.assertNotIn(self.linen_floral_dress_cornflower, filtered_qs)
        self.assertIn(self.linen_floral_dress_roses, filtered_qs)
        self.assertNotIn(self.sleeveless_dress_green, filtered_qs)

    def test_size_filter(self):
        f = ProductFilter(size=["2", "3"])
        filtered_qs = self.qs.filter(f.get_Q())
        self.assertIn(self.linen_floral_dress_cornflower, filtered_qs)
        self.assertNotIn(self.linen_floral_dress_roses, filtered_qs)
        self.assertNotIn(self.sleeveless_dress_green, filtered_qs)

        f = ProductFilter(size=["2"])
        filtered_qs = self.qs.filter(f.get_Q())
        self.assertEqual(filtered_qs.count(), 0)

    def test_invalid_pk_values(self):
        self.assertEqual(ProductFilter(size=["s", "3m"]).get_Q(), Q())
        self.assertEqual(ProductFilter(size=["s", "36"], color=['blue', 'red']).get_Q(), Q())
        self.assertEqual(ProductFilter(price=['25EUR'], disc_price=['']).get_Q(), Q())

    def test_combined(self):
        f = ProductFilter(price_gte=['69'], price_lte=['79'], color=['1', '3'])
        filtered_qs = self.qs.filter(f.get_Q())
        self.assertIn(self.linen_floral_dress_cornflower, filtered_qs)
        self.assertIn(self.linen_floral_dress_roses, filtered_qs)
        self.assertNotIn(self.sleeveless_dress_green, filtered_qs)
