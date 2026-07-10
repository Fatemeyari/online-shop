from shop.models import Product ,ProductStatusType

class CartSession:
    def __init__(self , session):
        self.session=session
        self._cart=self.session.setdefault("cart",
        {
            "items":[],
            "total_price":0,
            "total_items":0
        })


    def add_product(self, product_id):
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                item["quantity"]+=1
                break
        else:
            new_item={"product_id":product_id , "quantity":1}
            self._cart["items"].append(new_item)
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

    
    def save(self):
        self.session.modified=True

    









