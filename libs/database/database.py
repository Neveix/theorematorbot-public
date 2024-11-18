import sqlite3

class DataBase: 
    def __del__(self):
        if self.db:
            self.db.close()
            print("Database was successfully closed")

    def open(self, filePath):
        self.db = sqlite3.connect(filePath)
        self.create_table()

    def get_user_balance(self, telegramId):
        if not self.user_already_exists(telegramId):
            self.register_new_user(telegramId)
            return 0
        cursor = self.db.cursor()
        cursor.execute("SELECT balance FROM Users WHERE telegramId = ?", (telegramId,))
        balance = cursor.fetchone()[0]
        cursor.close()
        return balance

    def update_user_balance(self, telegramId, newBalance):
        cursor = self.db.cursor()
        cursor.execute("UPDATE Users SET balance = ? WHERE telegramId = ?", (newBalance, telegramId))
        self.db.commit()
        cursor.close()

    def create_table(self):
        self.db.execute("CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY, telegramId INT, balance INT)")

    def user_already_exists(self, telegramId):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM Users WHERE telegramId = ?", (telegramId,))
        exists = cursor.fetchone() is not None
        cursor.close()
        return exists

    def register_new_user(self, telegramId):
        self.db.execute("INSERT INTO Users (telegramId, balance) VALUES (?, ?)", (telegramId, 0))

# пример использования

# db = DataBase ()
# db.open("./database.db")
# print(db.get_user_balance(100))
# db.update_user_balance(100,100)
# print(db.get_user_balance(100))
