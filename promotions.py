from abc import ABC, abstractclassmethod

# interface of Promotion and Promotion Pipeline
class IPromotion():
    def __init__(self):
        pass

    def get_discount():
        pass


# 考量不同 promotion 類型, PromotionPipeline 可做成 interface,
# register 的參數也可再做一層抽象化成 Promotion的類型, 
# 於是在 pipeline 中可只決定不同類型的 Promotion 計算順序, 而非 object of promotion 的計算順序
# 但本題並未有多重 promotion 計算的情境, 為避免 overdesign, 先不採用上述寫法
class PromotionPipeline():
    def __init__(self):
        self.promotions = list()

    def register(self, promotion):
        """ 依序加入要計算的優惠方式 """
        self.promotions.append(promotion)

    def invoke(self, order):
        """執行多重優惠計算
        Returns:
            total_discount_money: 此訂單透過此優惠鏈總折扣價錢
            total_gift: 此訂單透過此優惠鏈得到的贈品
        """
        total_discount_money = 0  # init
        total_gifts = list()  # init

        for promotion in self.promotions:
            promotion.use_promotion(order)
            total_discount_money += promotion.discount_money
            total_gifts += promotion.gifts
        
        return total_discount_money, total_gifts
            

class TotalOrderDiscountPromotion(IPromotion):
    """ 訂單滿X折Z% """
    def __init__(self, x, z):
        self.x = x
        self.z = z

    def use_promotion(self, order):
        self.discount_money = 0
        self.gifts = list()
        if order.original_price >= self.x:
            self.discount_money =  int(order.original_price * (100-self.z) * 0.01)


class TotalOrderGiftPromotion(IPromotion):
    """ 訂單滿X贈送特定商品 """
    def __init__(self, x, gift):
        self.x = x
        self.gift = gift

    def use_promotion(self, order):
        self.discount_money = 0
        self.gifts = list()
        if order.original_price >= self.x:
            self.gifts.append(self.gift)


class SpecificCommodityPromotion(IPromotion):
    """ 特定商品滿 X 件折 Y 元 """
    def __init__(self, product_name, x, y):
        self.specific_product_name = product_name
        self.x = x
        self.y = y

    def use_promotion(self, order):
        self.discount_money = 0
        self.gifts = list()
        for product, amount in order.commodities_in_order.items():
            if (product.product_name == self.specific_product_name
                    and amount >= self.x):
                self.discount_money = self.y
                break


class TotalOrderCashBackPromotion(IPromotion):
    """  訂單滿 X 元折 Y 元,此折扣在全站總共只能套用 N 次"""
    def __init__(self, x, y, n):
        self.x = x
        self.y = y
        self.n = n  # 實際應用應存放在 Database 中, 但此處為了簡化寫法, 記錄在memory中

    def use_promotion(self, order):
        self.discount_money = 0
        self.gifts = list()
        if order.original_price >= self.x and self.n > 0:
            self.discount_money =  self.y
            self.n -= 1
    
