import pyrebase
import json

class DBhandler:

    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config = json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

    def insert_product(self, data, img_path):
        product_info = {
            "category": data['category'],
            "region": data['region'],
            "price": data['price'],
            "status": data['status'],
            "title": data['title'],
            "content": data['content'],
            "writerID": data['writerID'],
            "img_path": img_path
        }

        self.db.child("product").push(product_info)
        return True

    def insert_review(self, data, img_path):
        review_info = {
             "sellerID": data['sellerID'],
             "category": data['category'],
             "rate": data['rate'],
             "title": data['title'],
             "content": data['content'],
             "img_path": img_path,
             "writerID": data['writerID']
        }

        self.db.child("review").push(review_info)
        return True

    def insert_user(self, data, pw):
        user_info = {
            "id": data['username'],
            "pw": pw,
            "email": data['email'],
            "phone": data['phone'],
            "birthdate": data['birthdate']
        }
        if self.user_duplicate_check(str(data['username'])):
            self.db.child("user").push(user_info)
            print(data)
            return True
        else:
            return False

    def user_duplicate_check(self, id_string):
        users = self.db.child("user").get()

        print("users###", users.val())
        if str(users.val()) == "None":
            return True
        else:
            for res in users.each():
                value = res.val()
                if value['id'] == id_string:
                    return False
            return True
    
    def find_user(self, id_, pw_):
        users = self.db.child("user").get()
        target_value=[]
        for res in users.each():
            value = res.val()
            if value['id'] == id_ and value['pw'] == pw_:
                return True
        return False
    

    def get_products(self):
        products = self.db.child("product").get().val()
        return products

    def get_item_byname(self, name):
        items = self.db.child("product").get()
        target_value=""
        for res in items.each():
            key_value = res.key()
            
            if key_value == name:
                target_value=res.val()
        return target_value
    

    def get_reviews(self):
        reviews = self.db.child("review").get().val()
        return reviews

    def get_review_byname(self, name):
        items = self.db.child("review").get()
        target_value=""
        for res in items.each():
            key_value = res.key()
            
            if key_value == name:
                target_value=res.val()
        return target_value

    def get_heart_byname(self, uid, name):
        hearts = self.db.child("heart").child(uid).get()
        target_value=""
        if hearts.val() == None:
            return target_value
    
        for res in hearts.each():
            key_value = res.key()
        
            if key_value == name:
                target_value=res.val()
        return target_value
 
    def update_heart(self, user_id, isHeart, item):
        heart_info = {
        "interested": isHeart
        }
        self.db.child("heart").child(user_id).child(item).set(heart_info)
        return True
    
    def get_wishlist_items(self, user_id):
        wishlist_items = []
        user_wishlist = self.db.child("heart").child(user_id).get().val()

        if user_wishlist:
            for item_id, item_details in user_wishlist.items():
                interested_status = item_details.get("interested")
                if interested_status == "Y":
                    item_info = self.db.child("product").child(item_id).get().val()
                    if item_info:
                        item_info['key'] = item_id
                        wishlist_items.append(item_info)

        return wishlist_items
    
    def get_my_products(self, writer_id):
        my_products = []
        products = self.db.child("product").get().val()

        for key, product_info in products.items():
            if product_info.get("writerID") == writer_id:
                product_info['key'] = key
                my_products.append(product_info)
        
        print("My Products:", my_products)

        return my_products
    