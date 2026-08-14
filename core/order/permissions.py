from django.contrib.auth.mixins import UserPassesTestMixin

from accounts.models import UserType 
from cart.cart import CartSession

class HasCustomerAccessPermission(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.type == UserType.customer.value
        return False

class HasCartCustomerPermission(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if not user.is_authenticated :
            return False
        if user.type != UserType.customer.value :
            return False
        cart = CartSession(self.request.session)
        return bool(cart.get_cart_items())
  
