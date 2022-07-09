from django.urls import path
from .views import (add_to_productcart, change_productcart,
                    delete_productcart, get_productcart, cart_page, submit_order)


urlpatterns = [
    path('submit-cart/', submit_order, name='submit_order'),
    path('cart/', cart_page, name='cart_page'),
    path('get-cart/', get_productcart, name='get_productcart'),
    path('add-cart/', add_to_productcart, name='add_to_productcart'),
    path('update-cart/', change_productcart, name='change_productcart'),
    path('delete-cart/', delete_productcart, name='delete_productcart'),
]
