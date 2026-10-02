from abc import ABC, abstractmethod

class Product:
    def __init__(self,name,price,category):
        self.name = name
        self.price = price
        self.category= category

class CartItem:
    def __init__(self,product,quantity):
        self.product = product
        self.quantity = quantity

class Coupon(ABC):
    @abstractmethod
    def calculate_discount(self,cart,current_price):
        pass

class PercentageCoupon(Coupon):

    def __init__(self, percent_off):
        self.percent_off = percent_off

    def calculate_discount(self,cart,current_price):
        discount = current_price * (self.percent_off/100)
        return discount

class CategoryCoupon(Coupon):

    def __init__(self,category,percent_off):
        self.category = category
        self.percent_off = percent_off

    def calculate_discount(self,cart,current_price):
        discount = 0
        for cart_item in cart.get_items():
            if cart_item.product.category == self.category:
                discount += (self.percent_off / 100) * cart_item.product.price * cart_item.quantity
        return discount

class BOGOCoupon(Coupon):
    def calculate_discount(self,cart,current_price):
        discount = 0
        for cart_item in cart.get_items():
            free_items = cart_item.quantity // 2
            discount += free_items * cart_item.product.price
        return discount

class Cart:
    def __init__(self):
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
            if cart_item.product.name == new_item.product.name:
                cart_item.quantity+=new_item.quantity
                return

        self.cart_items.append(new_item)

    def remove_item(self,del_item):
        for item in self.cart_items:
            if item.product.name == del_item.product.name:
                item.quantity-=1
                if item.quantity == 0:
                    self.cart_items.remove(item)
            return
    
    def get_items(self):
        return self.cart_items

    def add_coupon(self,coupon):
        self.coupons_added.append(coupon)
    
    def remove_coupon(self,remove_coupon):
        for coupon in self.coupons_added:
            if coupon == remove_coupon:
                self.coupons_added.remove(remove_coupon)
        return

    def get_final_price(self):
        curr_price = self.get_sub_total()
        for coupon in self.coupons_added:
            curr_price -= coupon.calculate_discount(self,curr_price)
        return curr_price


if __name__ == "__main__":
    cart = Cart();
    laptop = Product("laptop",140,"Electronics")
    laptop_item = CartItem(laptop,2)
    tshirt  = Product("tshirt", 50 , "Clothing")

