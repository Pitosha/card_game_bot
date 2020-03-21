import database
import config as c

class User:

    def __init__(self, target_id):
        self.target_id = target_id

    def create_user(self, user_name):
        new_user = [(
            self.target_id,
            user_name,
            0,
            0
        )]
        db = database.Db(c.connect_db)
        db.create_user_on_db(new_user)

    def init_user(self, all_items="bool"):
        db = database.Db(c.connect_db)
        res = db.get_user_from_user_id(self.target_id, all_items)
        return res

    def get_all_users(self):
        db = database.Db(c.connect_db)
        res = db.get_all_users()
        return res

    def update_user(self, user_name, user_item, fall_item):
        up_user = [(
            user_name,
            user_item,
            fall_item,
            self.target_id
        )]
        db = database.Db(c.connect_db)
        db.update_user_on_db(up_user)

    def delete_user(self, user_id):
        pass