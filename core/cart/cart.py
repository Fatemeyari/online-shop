from shop.models import Product ,ProductStatusType
from .models import CartModel , CartItemModel
class CartSession:
    def __init__(self , session):
        self.session=session
        self._cart=self.session.setdefault("cart",
        {
            "items":[],
            "total_price":0,
            "total_items":0
        })


    def increase_stock(self,product_id , quantity):
        product_obj=Product.objects.get(id=product_id , status=ProductStatusType.publish.value)
        product_obj.stock += int(quantity)
        product_obj.save()

    def decrease_stock(self,product_id , quantity):
        product_obj=Product.objects.get(id=product_id , status=ProductStatusType.publish.value)
        if product_obj.stock >= quantity:
            product_obj.stock -= int(quantity) 
            product_obj.save()

    def add_product(self, product_id):
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                item["quantity"]+=1
                break
        else:
            new_item={"product_id":product_id , "quantity":1}
            self._cart["items"].append(new_item)

        self.decrease_stock(product_id , 1)
        self.save()

    def get_cart_items(self):
        for item in self._cart["items"]:
            product_obj=Product.objects.get(id=item["product_id"], status=ProductStatusType.publish.value)
            item.update({"product_obj":product_obj , "price":item["quantity"] * product_obj.get_price()})
        return self._cart["items"]


    def get_total_quantity(self):
        return sum(item["quantity"] for item in self._cart["items"])
    

    def get_total_price(self):
        return sum(item["price"] for item in self._cart["items"])


    def get_discount(self):
        discounts=0
        for item in self._cart["items"]:
            product_discount=Product.objects.get(id=item["product_id"] , status=ProductStatusType.publish.value).get_discount()
            discounts+= product_discount * item["quantity"]
            
        return round(discounts)

    def increase_product_quantity(self,product_id):
        product_obj=Product.objects.get(id=product_id , status=ProductStatusType.publish.value)
        for item in self._cart["items"]:
            if item["product_id"] == product_id:
                if product_obj.stock >0 : 
                    item["quantity"]+=1
                    self.decrease_stock(product_id , 1)
                    self.save()
                

    def decrease_product_quantity(self,product_id):
        for item in self._cart["items"]:
            if item["product_id"] == product_id:
                if item["quantity"] > 0:
                    item["quantity"] -=1
                    self.increase_stock(product_id , 1)
                    if item["quantity"]==0:
                        self._cart["items"].remove(item)

                else:
                    self._cart["items"].remove(item)
                break
        self.save()

    def remove_product(self,product_id):
        for item in self._cart["items"]:
            if item["product_id"] == product_id:
                self._cart["items"].remove(item)
                quantity=item["quantity"]
                self.increase_stock(product_id , quantity)
        self.save()  

    def sync_cart_items_from_db(self,user):
        cart , created= CartModel.objects.get_or_create(user=user)
        cart_items=CartItemModel.objects.filter(cart=cart)

        for cart_item in cart_items:
            for item in self._cart["items"]:
                if str(cart_item.product.id) == item["product_id"]:
                    cart_item.quantity = item["quantity"]
                    cart_item.save()
                    break
            else:
                new_item = {"product_id" : str(cart_item.product.id) , "quantity":cart_item.quantity}
                self._cart["items"].append(new_item)

        
    def merge_session_cart_in_db(self, user):
        cart , created= CartModel.objects.get_or_create(user=user)

        for item in self._cart["items"]:
            product_obj = Product.objects.get(id=item["product_id"] , status=ProductStatusType.publish.value)
            cart_item , created = CartItemModel.objects.get_or_create(cart=cart , product=product_obj)
            cart_item.quantity=item["quantity"]
            cart_item.save()

        session_product_ids= [item["product_id"] for item in self._cart["items"]]   
        CartItemModel.objects.filter(cart=cart).exclude(product__id__in=session_product_ids).delete()



    def save(self):
        self.session.modified=True

    









