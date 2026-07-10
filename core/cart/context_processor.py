from .cart import CartSession

def cart_processor(request):
    cart=request.session.get("cart")
    if not cart:
        cart=CartSession(request.session)
    return {"cart" : cart}
