from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from mptt.admin import DraggableMPTTAdmin

from . import models


class ProductInline(admin.TabularInline):
    model = models.Product
    extra = 6
    verbose_name = _("Product")
    verbose_name_plural = _("Products")


class StockInline(admin.TabularInline):
    model = models.Stock
    extra = 8
    verbose_name = _("Stock")
    verbose_name_plural = _("Stock")


class SizesInline(admin.TabularInline):
    model = models.Size
    extra = 8

    verbose_name = _("Size")
    verbose_name_plural = _("Sizes")


class SubCategoryInline(admin.TabularInline):
    model = models.Category
    extra = 4
    verbose_name = _("Subcategory")
    verbose_name_plural = _("Subcategories")


@admin.register(models.ParentProduct)
class ParentProductModelAdmin(admin.ModelAdmin):
    model = models.ParentProduct
    inlines = [ProductInline]
    list_display = ['name', 'category']
    search_fields = ['name', 'description']


@admin.register(models.Product)
class ProductModelAdmin(admin.ModelAdmin):
    model = models.Product
    inlines = [StockInline]
    list_display = [
        'parent', 'style', 'color', 'price', 'discounted_price', 'views'
    ]
    ordering = ['parent']
    search_fields = ['parent__name', 'parent__id', "style"]


@admin.register(models.Category)
class CategoryModelAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 20
    inlines = [SubCategoryInline]


@admin.register(models.SizeGroup)
class SizeGroupModelAdmin(admin.ModelAdmin):
    inlines = [SizesInline]


@admin.register(models.Size)
class SizeModelAdmin(admin.ModelAdmin):
    model = models.Size
    list_display = ['name', 'group']
    search_fields = ['name', 'group']


@admin.register(models.Color)
class ColorModelAdmin(admin.ModelAdmin):
    model = models.Color
    list_display = ['name', 'hex_code']
    search_fields = ['name', 'hex_code']


@admin.register(models.Stock)
class StockModelAdmin(admin.ModelAdmin):
    model = models.Stock
    list_display = ['id', 'product', 'size', "quantity"]
    search_fields = ['id', 'product', 'size', "quantity"]


@admin.register(models.Image)
class ImageModelAdmin(admin.ModelAdmin):
    model = models.Image
    list_display = ['id', 'product', 'url']
    search_fields = ['product']






