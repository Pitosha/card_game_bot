import database
import config as c

class Chat:
    
    def __init__(self, target_id):
        self.target_id = target_id

    def create_chat(self, chat_name, game_state, user_one, user_two, user_one_item=0, user_two_item=0, game_table_msg_id=0,  user_one_is_ready=0,  user_two_is_ready=0):
        new_chat = [(
            self.target_id,
            chat_name,
            game_state,
            user_one,
            user_two,
            user_one_item,
            user_two_item,
            game_table_msg_id,
            user_one_is_ready,
            user_two_is_ready
        )]
        db = database.Db(c.connect_db)
        db.create_chat_on_db(new_chat)

    def init_chat(self, all_items="bool"):
        db = database.Db(c.connect_db)
        res = db.get_chat_from_chat_id(self.target_id, all_items)
        return res

    def update_chat(self, chat_name, game_state, user_one, user_two, user_one_item, user_two_item,game_table_msg_id, user_one_is_ready, user_two_is_ready):
        up_chat = [(
            chat_name,
            game_state,
            user_one,
            user_two,
            user_one_item,
            user_two_item,
            game_table_msg_id,
            user_one_is_ready,
            user_two_is_ready,
            self.target_id
        )]
        db = database.Db(c.connect_db)
        db.update_chat_on_db(up_chat)

    def delete_chat(self):
        del_chat = [(
            self.target_id
        )]
        db = database.Db(c.connect_db)
        db.delete_chat_on_db(del_chat)