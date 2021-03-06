from django.conf.urls import url
from .views import view_cart, add_to_cart, adjust_cart

urlpatterns = [
    url(r'^$', view_cart, name='view_cart'),
    url(r'^add/(?P<id>\d+)', add_to_cart, name='add_to_cart'), # allow an id number
    url(r'^adjust/(?P<id>\d+)$', adjust_cart, name='adjust_cart'), # adjust qties within a cart
    ]