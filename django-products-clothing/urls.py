from django.urls import re_path, path

from . import views

urlpatterns = [
    re_path(r'^p/(?P<slug>[-\w]+)/$', views.ProductDetail.as_view(), name='product_detail'),
    path('', views.ProductList.as_view(), name='product_list'),
    re_path(r'^(?P<path>[\w/-]+)/$', views.ProductByCategoryList.as_view(), name='product_by_category_list'),
]

