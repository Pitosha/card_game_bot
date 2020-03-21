import MySQLdb
import gc

class Db:
    def __init__(self, connect_db):
        try:
            self.conn = MySQLdb.connect(connect_db[0], connect_db[1], connect_db[2], connect_db[3],
                                        use_unicode=True, charset="utf8mb4")
            self.cursor = self.conn.cursor()
        except Exception:
            self.conn.close()
            gc.collect()
            print("Ошибка подключения БД")

    #Блок обработка таблицы чата


    #Регистрация чата в БД
    def create_chat_on_db(self, new_chat):
        self.cursor.executemany("INSERT INTO chat(chat_id, chat_name, game_state, user_one, user_two,user_one_item, user_two_item, game_table_msg_id, user_one_is_ready, user_two_is_ready) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", new_chat)
        self.conn.commit()
        self.conn.close()
        gc.collect()

    #Обновление ячейки чата по id
    def update_chat_on_db(self, up_chat):
        self.cursor.executemany("""UPDATE chat SET chat_name=%s, game_state=%s, user_one=%s, user_two=%s, user_one_item=%s, user_two_item=%s, game_table_msg_id=%s, user_one_is_ready=%s, user_two_is_ready=%s WHERE chat_id=%s""", (up_chat))
        self.conn.commit()
        self.conn.close()
        gc.collect()

    #возвращает чат по id чата
    def get_chat_from_chat_id(self, chat_id, all_items):
        self.cursor.execute("SELECT chat_id, chat_name, game_state, user_one, user_two, user_one_item, user_two_item, game_table_msg_id, user_one_is_ready, user_two_is_ready FROM chat WHERE chat_id={}".format(str(chat_id)))
        res = self.cursor.fetchall()

        if len(res) == 0:
            self.conn.close()
            gc.collect()
            return False
        else:
            if all_items == "obj":
                self.conn.close()
                gc.collect()
                return res[0]
            elif all_items == "bool":
                self.conn.close()
                gc.collect()
                return True


    def delete_chat_on_db(self, chat_id):
        self.cursor.execute("""DELETE FROM chat WHERE chat_id=%s""", (chat_id))
        self.conn.commit()
        self.conn.close()
        gc.collect()






    #Блок обработка таблицы юзера
    def create_user_on_db(self, new_user):
        self.cursor.executemany("INSERT INTO user(user_id, user_name, user_item, fall_item) VALUES(%s, %s, %s, %s)", new_user)
        self.conn.commit()
        self.conn.close()
        gc.collect()


    #возвращает юзера по id юзера
    def get_user_from_user_id(self, user_id, all_items):
        self.cursor.execute("SELECT user_id, user_name, user_item, fall_item FROM user WHERE user_id={}".format(str(user_id)))
        res = self.cursor.fetchall()

        if len(res) == 0:
            self.conn.close()
            gc.collect()
            return False
        else:
            if all_items == "obj":
                self.conn.close()
                gc.collect()
                return res[0]
            elif all_items == "bool":
                self.conn.close()
                gc.collect()
                return True

    #Возвращает всех юзеров
    def get_all_users(self):
        self.cursor.execute("SELECT user_id, user_name, user_item, fall_item FROM user")
        res = self.cursor.fetchall()
        return res


    #Обновление ячейки юзера по id
    def update_user_on_db(self, up_user):
        self.cursor.executemany("""UPDATE user SET user_name=%s, user_item=%s, fall_item=%s WHERE user_id=%s""", (up_user))
        self.conn.commit()
        self.conn.close()
        gc.collect()