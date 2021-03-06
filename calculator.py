from model import Product
from model import User


class Order():
    def __init__(self, customer: User):
        self.order_id = "uuid"  # 在此不實作取得 uuid 的方式
        self.customer = customer
        self.commodities_in_order = dict()  # {product_name: amount}
        self.original_price = 0

    def add_commodity(self, commodity: Product, amount: int):
        if commodity in self.commodities_in_order:
            self.commodities_in_order[commodity] += amount
        else:
            self.commodities_in_order.update({commodity: amount})

        self.original_price += commodity.price * amount


class Calculator():
    def __init__(self, order_to_be_calculated: Order):
        self.order = order_to_be_calculated
        self.original_total_price = self.order.original_price
        self.total_discount_money = 0
        self.total_gifts = list()

    def use_total_promotion(self, promotion_pipeline):
        self.total_discount_money, self.total_gifts = promotion_pipeline.invoke(self.order)
        
