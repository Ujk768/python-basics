
class Product:
    def __init__(self,name,price,category):
        self.name = name
        self.price = price
        self.category= category

class CartItem:
    def __init__(self,product,quantity):
        self.product = product
        self.quantity = quantity


class Cart:
    def __init__(self,cartItems,coupons):
        self.cart_items = []
        self.coupons_added = []
    
    def get_sub_total(self):
        sub_total =0
        for item in self.cart_items:
            price = item.product.price * item.quantity
            sub_total += price
        return sub_total
        
    def add_item(self,new_item):
        for cart_item in self.cart_items:
            if cart_item.product.name == new_item.name:
                item.quantity+=new_item.quantity
                return

        self.cart_items.append(new_item)

    def remove_item(self,del_item):
        for items in self.cart_items:
            if item.name == del_item.name:
                item.quantity-=1
    
        




if __name__ == "__main__":
    cart = Cart([],[]);
    laptop = Product("laptop",140,"Electronics")
    laptop_item = CartItem(laptop,2)
    cart.add_item(laptop_item)
    print(cart.get_sub_total())

