from django.urls import path
from .views import (home, discount, productdetail, productdetailinfo, catlist,
                    childcat, catdetail, getcatchild, get_catchild_details,
                    productlist, Search_product, Get_product_in_category, getbrand, getseller, getgeneralspecifications)

urlpatterns = [
    path('', home, name='home'),
    path('disc/', discount, name='discount'),
    path('categorys/', catlist, name='catlist'),
    path('searchproduct/', Search_product.as_view(), name='search_product'),
    path('getcatchilds/', getcatchild, name='getcatchild'),
    path('get-catchilds-details/', get_catchild_details, name='get_catchild_details'),
    path('catchilds/', childcat, name='childcat'),
    path('productdetail/<int:id>/', productdetail, name='productdetails'),
    path('catdetails/<int:id>/', catdetail, name='catdet'),
    path('productlist_details/<int:id>/', productlist, name='productlist'),
    path('productinfo/', productdetailinfo, name='productinfo'),
    path('products/', Get_product_in_category.as_view(), name='get_product_in_category'),
    path('brands/', getbrand, name='getbrand'),
    path('sellers/', getseller, name='getseller'),
    path('generalspecifications/', getgeneralspecifications, name='getgeneralspecifications'),
]
