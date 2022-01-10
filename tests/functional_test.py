import pytest

from caculator import Product, Order, Caculator
from model import User, Product
from promotions import (TotalOrderDiscountPromotion, PromotionPipeline, SpecificCommodityPromotion
        ,TotalOrderGiftPromotion, TotalOrderCashBackPromotion)


# 模擬利用 DAO  取得 data model
# 建立三種商品: book, pen, notebook, 價格分別為100, 30, 50
book = Product('book', 100)
pen = Product('pen', 30)
notebook = Product('notebook', 50)

@pytest.fixture()
def alans_order():
    alans_order = Order()
    alans_order.add_commodity(book, 5)
    alans_order.add_commodity(pen, 3)
    alans_order.add_commodity(notebook, 2)
    return alans_order


class TestPromotions():
    def test_generate_a_new_order(self):
        alans_order = Order()
        assert len(alans_order.commodities_in_order) == 0 


    def test_receivable_x_and_discount(self, alans_order):
        """  訂單滿 X 元折 Z % """
        caculator = Caculator(alans_order)
        expected_total_price = 690
        actual_total_price = caculator.original_total_price
        assert expected_total_price == actual_total_price

        promotion1  = TotalOrderDiscountPromotion(x=500, z=10)  # 訂單滿500折10%

        promotion_pipeline = PromotionPipeline()
        promotion_pipeline.register(promotion1)  

        caculator.use_total_promotion(promotion_pipeline)

        actual_total_discount_money = caculator.total_discount_money
        expected_total_discount_money = 621
        assert expected_total_discount_money == actual_total_discount_money


    def test_commodity_quantity_x_and_y_dollar_off(self, alans_order):
        """ 特定商品滿 X 件折 Y 元 """
        caculator = Caculator(alans_order)
        expected_total_price = 690
        actual_total_price = caculator.original_total_price
        assert expected_total_price == actual_total_price

        promotion2  = SpecificCommodityPromotion('book', x=4, y=5)  # book滿4件折5元

        promotion_pipeline = PromotionPipeline()
        promotion_pipeline.register(promotion2)  

        caculator.use_total_promotion(promotion_pipeline)

        actual_total_discount_money = caculator.total_discount_money
        expected_total_discount_money = 5
        assert expected_total_discount_money == actual_total_discount_money


    def test_receivable_x_and_give_away(self, alans_order):
        """ 訂單滿 X 元贈送特定商品 """
        caculator = Caculator(alans_order)
        expected_total_price = 690
        actual_total_price = caculator.original_total_price
        assert expected_total_price == actual_total_price

        promotion3  = TotalOrderGiftPromotion(x=500, gift='eraser')  # 訂單滿100送橡皮擦

        promotion_pipeline = PromotionPipeline()
        promotion_pipeline.register(promotion3)

        caculator.use_total_promotion(promotion_pipeline)

        actual_gifts = caculator.total_gifts
        expected_gift = 'eraser'
        assert expected_gift in actual_gifts


    def test_receivable_x_and_y_dollar_off(self, alans_order):
        caculator = Caculator(alans_order)
        expected_total_price = 690
        actual_total_price = caculator.original_total_price
        assert expected_total_price == actual_total_price

        promotion4  = TotalOrderCashBackPromotion(x=400, y=12, n=2)  # 訂單滿400折12, 全站只能用兩次
        
        promotion_pipeline = PromotionPipeline()
        promotion_pipeline.register(promotion4)

        caculator.use_total_promotion(promotion_pipeline)

        actual_total_discount_money = caculator.total_discount_money
        expected_total_discount_money = 12
        assert expected_total_discount_money == actual_total_discount_money

        # 另一新訂單: Judy's order
        judys_order = Order()
        judys_order.add_commodity(book, 7)
        judys_order.add_commodity(pen, 3)
        judys_order.add_commodity(notebook, 0)

        caculator2 = Caculator(judys_order)
        print(caculator2.total_discount_money)
        print(judys_order.original_price)
        caculator2.use_total_promotion(promotion_pipeline)

        actual_total_discount_money = caculator2.total_discount_money
        expected_total_discount_money = 12
        assert expected_total_discount_money == actual_total_discount_money

        # 第三筆訂單: Tim's order, 此時優惠用光了, 所以 discount_money == 0
        tims_order = Order()
        tims_order.add_commodity(book, 2)
        tims_order.add_commodity(pen, 1)
        tims_order.add_commodity(notebook, 0)

        caculator3 = Caculator(tims_order)
        caculator3.use_total_promotion(promotion_pipeline)

        actual_total_discount_money = caculator3.total_discount_money
        expected_total_discount_money = 0
        assert expected_total_discount_money == actual_total_discount_money


        