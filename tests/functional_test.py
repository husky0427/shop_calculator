import pytest

from calculator import Product, Order, Calculator
from model import User, Product
from promotions import (TotalOrderDiscountPromotion, PromotionPipeline, SpecificCommodityPromotion, TotalOrderDiscountPersonalLimitPromotion
        ,TotalOrderGiftPromotion, TotalOrderCashBackPromotion)


# 模擬利用 DAO  取得 data model
# 建立三種商品: book, pen, notebook, 價格分別為100, 30, 50
book = Product('book', 100)
pen = Product('pen', 30)
notebook = Product('notebook', 50)

@pytest.fixture()
def alans_order():
    alan = User('Alan')
    alans_order = Order(alan)
    alans_order.add_commodity(book, 5)
    alans_order.add_commodity(pen, 3)
    alans_order.add_commodity(notebook, 2)
    return alans_order


class TestPromotions():
    def test_generate_a_new_order(self):
        bob = User('Bob')
        bob_order = Order(bob)
        assert len(bob_order.commodities_in_order) == 0 


    def test_receivable_x_and_discount(self, alans_order):
        """  訂單滿 X 元折 Z % """
        calculator = Calculator(alans_order)
        expected_total_price = 690
        actual_total_price = calculator.original_total_price
        assert expected_total_price == actual_total_price

        promotion1  = TotalOrderDiscountPromotion(x=500, z=10)  # 訂單滿500折10%

        promotion_pipeline = PromotionPipeline()
        promotion_pipeline.register(promotion1)  

        calculator.use_total_promotion(promotion_pipeline)

        actual_total_discount_money = calculator.total_discount_money
        expected_total_discount_money = 621
        assert expected_total_discount_money == actual_total_discount_money


    def test_commodity_quantity_x_and_y_dollar_off(self, alans_order):
        """ 特定商品滿 X 件折 Y 元 """
        calculator = Calculator(alans_order)
        expected_total_price = 690
        actual_total_price = calculator.original_total_price
        assert expected_total_price == actual_total_price

        promotion2  = SpecificCommodityPromotion('book', x=4, y=5)  # book滿4件折5元

        promotion_pipeline = PromotionPipeline()
        promotion_pipeline.register(promotion2)  

        calculator.use_total_promotion(promotion_pipeline)

        actual_total_discount_money = calculator.total_discount_money
        expected_total_discount_money = 5
        assert expected_total_discount_money == actual_total_discount_money


    def test_receivable_x_and_give_away(self, alans_order):
        """ 訂單滿 X 元贈送特定商品 """
        calculator = Calculator(alans_order)
        expected_total_price = 690
        actual_total_price = calculator.original_total_price
        assert expected_total_price == actual_total_price

        promotion3  = TotalOrderGiftPromotion(x=500, gift='eraser')  # 訂單滿100送橡皮擦

        promotion_pipeline = PromotionPipeline()
        promotion_pipeline.register(promotion3)

        calculator.use_total_promotion(promotion_pipeline)

        actual_gifts = calculator.total_gifts
        expected_gift = 'eraser'
        assert expected_gift in actual_gifts


    def test_receivable_x_and_y_dollar_off(self, alans_order):
        calculator = Calculator(alans_order)
        expected_total_price = 690
        actual_total_price = calculator.original_total_price
        assert expected_total_price == actual_total_price

        promotion4  = TotalOrderCashBackPromotion(x=400, y=12, n=2)  # 訂單滿400折12, 全站只能用兩次
        
        promotion_pipeline = PromotionPipeline()
        promotion_pipeline.register(promotion4)

        calculator.use_total_promotion(promotion_pipeline)

        actual_total_discount_money = calculator.total_discount_money
        expected_total_discount_money = 12
        assert expected_total_discount_money == actual_total_discount_money

        # 另一新訂單: Judy's order
        judy = User('Judy')
        judys_order = Order(judy)
        judys_order.add_commodity(book, 7)
        judys_order.add_commodity(pen, 3)
        judys_order.add_commodity(notebook, 0)

        calculator2 = Calculator(judys_order)
        print(calculator2.total_discount_money)
        print(judys_order.original_price)
        calculator2.use_total_promotion(promotion_pipeline)

        actual_total_discount_money = calculator2.total_discount_money
        expected_total_discount_money = 12
        assert expected_total_discount_money == actual_total_discount_money

        # 第三筆訂單: Tim's order, 此時優惠用光了, 所以 discount_money == 0
        tim = User('Tim')
        tims_order = Order(tim)
        tims_order.add_commodity(book, 2)
        tims_order.add_commodity(pen, 1)
        tims_order.add_commodity(notebook, 0)

        calculator3 = Calculator(tims_order)
        calculator3.use_total_promotion(promotion_pipeline)

        actual_total_discount_money = calculator3.total_discount_money
        expected_total_discount_money = 0
        assert expected_total_discount_money == actual_total_discount_money


    def test_receivable_x_discount_personal_limit(self, alans_order):
        """ (加分題)訂單滿 X 元折 Z %,折扣每人只能總共優惠 N 元 """
        calculator = Calculator(alans_order)
        expected_total_price = 690
        actual_total_price = calculator.original_total_price
        assert expected_total_price == actual_total_price

        promotion5  = TotalOrderDiscountPersonalLimitPromotion(x=200, z=0.90, n=50)  # 訂單滿200, 9折, 每個人上限50

        promotion_pipeline = PromotionPipeline()
        promotion_pipeline.register(promotion5)

        calculator.use_total_promotion(promotion_pipeline)

        actual_total_discount_money = calculator.total_discount_money
        expected_total_discount_money = 50
        assert expected_total_discount_money == actual_total_discount_money

        # 建立第二個人 Julia 的訂單, 其 quota 都未曾使用過
        julia = User('Julia')
        julias_order = Order(julia)
        julias_order.add_commodity(book, 2)
        julias_order.add_commodity(notebook, 2)

        calculator2 = Calculator(julias_order)
        calculator2.use_total_promotion(promotion_pipeline)

        actual_total_discount_money = calculator2.total_discount_money
        expected_total_discount_money = 30
        assert expected_total_discount_money == actual_total_discount_money


