from django.urls import path
from .views import like, bookmark, bookmarkdisplay, likedisplay, cumment, cummentdisplay


urlpatterns = [
    path('display-cummnet/', cummentdisplay, name='cummentdisplay'),
    path('add-cummnet/', cumment, name='cumment'),
    path('like-display/', likedisplay, name='likedisplay'),
    path('bookmark-display/', bookmarkdisplay, name='bookmarkdisplay'),
    path('like-product/', like, name='like'),
    path('bookmark-product/', bookmark, name='bookmark'),
]
