from sqlite3 import Cursor, connect

PAYMENT_PURPOSE_REGULAR = 0
PAYMENT_PURPOSE_PREMIUM = 1
PAYMENT_PURPOSE_SUPPORT = 2

class GlobalUserDataManager:
    def __init__(self, path: str):
        self.con = connect(path)
        self.table_name_main = "UserTable"
        self.table_name_payments = "PaymentsTable"
        self.table_name_operations = "OperationsTable"
        self.table_static_values = "StaticValuesTable"
    def create_tables(self):
        cur = self.con.cursor()
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.table_name_main} (
 user_id INTEGER PRIMARY KEY NOT NULL
,first_name TEXT NOT NULL DEFAULT ''
,last_name TEXT
,username TEXT
,balance INTEGER NOT NULL DEFAULT 0
,is_premium INTEGER NOT NULL DEFAULT 0
,premium_subscripted_at INTEGER NOT NULL DEFAULT 0
,premium_subscription_payment TEXT NOT NULL DEFAULT ''
,is_support INTEGER NOT NULL DEFAULT 0
,support_subscripted_at INTEGER NOT NULL DEFAULT 0
,support_subscription_payment TEXT NOT NULL DEFAULT ''
)""")
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.table_name_payments} (
 user_id INTEGER NOT NULL
,payment_id TEXT NOT NULL
,created_at INTEGER NOT NULL
,succeeded INTEGER NOT NULL DEFAULT 0
,payment_purpose INTEGER NOT NULL DEFAULT 0
)""")
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.table_name_operations} (
 user_id INTEGER NOT NULL
,operation_id INTEGER NOT NULL
,performed_at INTEGER NOT NULL
)""")
        
        cur.close()
        self.con.commit()
    def create_user(self, user_id: int, cursor: Cursor | None = None):
        needs_close_cursor = False
        if cursor is None:
            cursor = self.con.cursor()
            needs_close_cursor = True
        result = cursor.execute(f"SELECT user_id FROM {self.table_name_main} WHERE user_id = ?", (user_id,)).fetchall()
        if result == []:
            cursor.execute(f"INSERT INTO {self.table_name_main} (user_id) VALUES (?)",(user_id,))
        if needs_close_cursor:
            cursor.close()
    def user_names_set(self, user_id: int, first_name: str, last_name: str, username: str) -> None:
        cur = self.con.cursor()
        self.create_user(user_id, cur)
        cur.execute(f"UPDATE {self.table_name_main} SET \
            first_name = ?, last_name = ?, username = ? WHERE user_id = ?", 
            (first_name, last_name, username, user_id))
        cur.close()
        self.con.commit()
    def user_names_get(self, user_id: int) -> tuple[str,str | None,str | None] | None:
        """result = tuple[first_name, last_name, username]"""
        cur = self.con.cursor()
        self.create_user(user_id, cur)
        result =  cur.execute(f"SELECT first_name, last_name, username FROM {self.table_name_main} \
WHERE user_id = ?", (user_id,)).fetchall()
        return result[0]

    
    def payment_add(self, user_id: int, payment_id: str, payment_purpose: int) -> None:
        cur = self.con.cursor()
        from time import time
        cur.execute(f"INSERT INTO {self.table_name_payments} (user_id, payment_id, created_at, payment_purpose) VALUES \
(?, ?, ?, ?)", (user_id, payment_id, int(time()), payment_purpose))
        cur.close()
        self.con.commit()
    def payment_remove(self, payment_id: str) -> None:
        cur = self.con.cursor()
        cur.execute(f"DELETE FROM {self.table_name_payments} WHERE payment_id = ?", (payment_id,))
        cur.close()
        self.con.commit()
    def payment_set_succeeded(self, payment_id: str) -> None:
        cur = self.con.cursor()
        cur.execute(f"UPDATE {self.table_name_payments} SET succeeded = 1 WHERE payment_id = ?",\
(payment_id,))
    def payment_get_not_succeeded(self) -> list[tuple[int, str, int, int]]:
        "result = list[tuple[user_id, payment_id, created_at, payment_purpose]]"
        cur = self.con.cursor() 
        result = cur.execute(f"SELECT user_id, payment_id, created_at, payment_purpose FROM {self.table_name_payments} \
WHERE succeeded = 0").fetchall()
        cur.close() 
        return result
    def payments_remove_old(self, threshold: int = 20*60):
        cur = self.con.cursor() 
        from time import time
        cur.execute(f"DELETE FROM {self.table_name_payments} WHERE created_at < ?",(time()-threshold,))
        cur.close() 
        self.con.commit()
    def operation_add(self, user_id: int, operation_id: int, performed_at: int) -> None:
        cur = self.con.cursor()
        cur.execute(f"INSERT INTO {self.table_name_operations} (user_id, operation_id, performed_at) \
VALUES (?, ?, ?)", (user_id, operation_id, performed_at))
        cur.close()
        self.con.commit()
    def operation_count(self, user_id: int, operation_id: int, max_time: int) -> int:
        cur = self.con.cursor()
        from time import time
        performed_max_time = int(time()) - max_time
        result = cur.execute(f"SELECT COUNT(*) FROM {self.table_name_operations} \
WHERE user_id = ? AND operation_id = ? AND performed_at < ?", (user_id, operation_id, performed_max_time)).fetchall()
        cur.close()
        return result[0][0]
    def operation_remove(self, user_id: int, operation_id: int) -> None:
        cur = self.con.cursor()
        cur.execute(f"DELETE FROM {self.table_name_operations} WHERE user_id = ? AND  \
operation_id = ?", (user_id, operation_id))
        cur.close()
        self.con.commit()
    def user_balance_set(self, user_id: int, balance: int) -> None:
        cur = self.con.cursor()
        self.create_user(user_id, cur)
        cur.execute(f"UPDATE {self.table_name_main} SET balance = ? WHERE user_id = ?", (balance, user_id))
        cur.close()
        self.con.commit()
    def user_balance_get(self, user_id: int) -> int:
        cur = self.con.cursor()
        self.create_user(user_id, cur)
        result = cur.execute(f"SELECT balance FROM {self.table_name_main} WHERE user_id = ?", (user_id,)).fetchall()
        cur.close()
        return result[0][0]
    def user_balance_add(self, user_id: int, value: int) -> None:
        balance = self.user_balance_get(user_id)
        self.user_balance_set(user_id, balance + int(float(value)))
        
    
    def premium_get(self, user_id: int) -> tuple[bool, int, str]:
        """result = tuple[is_premium, premiums_subscripted_at, premium_subscription_payment]"""
        cur = self.con.cursor()
        self.create_user(user_id, cur)
        result = cur.execute(f"SELECT is_premium, premium_subscripted_at, premium_subscription_payment \
FROM {self.table_name_main} WHERE user_id = ?", (user_id,)).fetchall()[0]
        cur.close()
        is_premium, i2, i3 = result
        return (bool(is_premium), i2, i3)
    def premium_activate(self, user_id: int, subscripted_at: int, premium_subscription_payment: str) -> None:
        cur = self.con.cursor()
        self.create_user(user_id, cur)
        cur.execute(f"UPDATE {self.table_name_main} SET premium_subscripted_at = ?, is_premium = 1, \
premium_subscription_payment = ? WHERE user_id = ?", (subscripted_at, premium_subscription_payment, user_id))
        cur.close()
        self.con.commit()
    def premium_deactivate(self, user_id: int) -> None:
        cur = self.con.cursor()
        self.create_user(user_id, cur)
        cur.execute(f"UPDATE {self.table_name_main} SET is_premium = 0 WHERE user_id = ?",
(user_id,))
        self.con.commit()
    def premium_get_old(
            self, 
            premium_time: int = 60*60*24*30
        ) -> list[tuple[int, str]]:
        "result = list[tuple[user_id, premium_subscription_payment]]"
        cur = self.con.cursor()
        from time import time
        result = cur.execute(f"SELECT user_id, premium_subscription_payment FROM {self.table_name_main} \
            WHERE is_premium = 1 AND premium_subscripted_at < ?", 
            (time()-premium_time,)).fetchall()
        cur.close()
        return result
    def premium_update_time(self, user_id: int):
        cur = self.con.cursor()
        from time import time
        cur.execute(f"UPDATE {self.table_name_main} SET premium_subscripted_at = ? WHERE user_id = ?",
            (int(time()), user_id))
        cur.close()
        self.con.commit()
    
    
    def support_get(self, user_id: int) -> tuple[bool, int, str]:
        """result = tuple[is_support, support_subscripted_at, support_subscription_payment]"""
        cur = self.con.cursor()
        self.create_user(user_id, cur)
        result = cur.execute(f"SELECT is_support, support_subscripted_at, support_subscription_payment \
FROM {self.table_name_main} WHERE user_id = ?", (user_id,)).fetchall()[0]
        cur.close()
        is_support, i2, i3 = result
        return (bool(is_support), i2, i3)
    def support_activate(self, user_id: int, subscripted_at: int, support_subscription_payment: str) -> None:
        cur = self.con.cursor()
        self.create_user(user_id, cur)
        cur.execute(f"UPDATE {self.table_name_main} SET support_subscripted_at = ?, is_support = 1, \
support_subscription_payment = ? WHERE user_id = ?", (subscripted_at, support_subscription_payment, user_id))
        cur.close()
        self.con.commit()
    def support_deactivate(self, user_id: int) -> None:
        cur = self.con.cursor()
        self.create_user(user_id, cur)
        cur.execute(f"UPDATE {self.table_name_main} SET is_support = 0 WHERE user_id = ?",
(user_id,))
        self.con.commit()
