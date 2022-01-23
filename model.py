
class User():
    LAST_ID = 0

    def __init__(self, user_name):
        # 實際應用應存放在 Database 中, 但此處為了簡化寫法, 記錄在memory中
        User.LAST_ID += 1
        self.user_id = User.LAST_ID
        self.user_name = user_name

class Product():
    def __init__(self, product_name, price):
        self.product_name = product_name
        self.price = price

