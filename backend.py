import os
import sqlite3
from random import choice, randint, shuffle

from cryptography.fernet import Fernet


class PasswordManagerBE:
    DB_FILE = "password_data.db"
    KEY_FILE = "secret.key"

    def __init__(self):
        self.cipher = Fernet(self._load_or_create_key())
        self._create_table()

    # ------------------------------------------------------------------
    # إعداد التشفير وقاعدة البيانات
    # ------------------------------------------------------------------
    def _load_or_create_key(self):
        """يحمّل مفتاح التشفير إن وُجد، أو ينشئ واحداً جديداً."""
        if os.path.exists(self.KEY_FILE):
            with open(self.KEY_FILE, "rb") as key_file:
                return key_file.read()
        key = Fernet.generate_key()
        with open(self.KEY_FILE, "wb") as key_file:
            key_file.write(key)
        return key

    def _connect(self):
        return sqlite3.connect(self.DB_FILE)

    def _create_table(self):
        with self._connect() as connection:
            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS Passwords (
                            Id INTEGER PRIMARY KEY AUTOINCREMENT,
                            Website TEXT UNIQUE,
                            Email TEXT,
                            Password TEXT)''')
            connection.commit()

    # ------------------------------------------------------------------
    # عمليات التشفير
    # ------------------------------------------------------------------
    def _encrypt(self, plain_text):
        return self.cipher.encrypt(plain_text.encode()).decode()

    def _decrypt(self, encrypted_text):
        return self.cipher.decrypt(encrypted_text.encode()).decode()

    # ------------------------------------------------------------------
    # عمليات قاعدة البيانات
    # ------------------------------------------------------------------
    def website_exists(self, website):
        with self._connect() as connection:
            cursor = connection.cursor()
            cursor.execute('''SELECT 1 FROM Passwords WHERE Website = ?''', (website,))
            return cursor.fetchone() is not None

    def save_data(self, website, email, password):
        encrypted_password = self._encrypt(password)
        with self._connect() as connection:
            cursor = connection.cursor()
            # INSERT OR REPLACE: إذا الموقع موجود مسبقاً، يستبدل بياناته بدل رفض العملية
            cursor.execute('''INSERT OR REPLACE INTO Passwords (Website, Email, Password)
                            VALUES (?, ?, ?)''', (website, email, encrypted_password))
            connection.commit()

    def search_password(self, website):
        with self._connect() as connection:
            cursor = connection.cursor()
            cursor.execute('''SELECT * FROM Passwords WHERE Website = ?''', (website,))
            result = cursor.fetchone()

        if result is None:
            return None

        record_id, site, email, encrypted_password = result
        decrypted_password = self._decrypt(encrypted_password)
        return (record_id, site, email, decrypted_password)

    def get_all_websites(self):
        """يُرجع قائمة بكل المواقع المحفوظة (مفيد لقوائم اقتراح أو عرض)."""
        with self._connect() as connection:
            cursor = connection.cursor()
            cursor.execute('''SELECT Website FROM Passwords ORDER BY Website''')
            return [row[0] for row in cursor.fetchall()]

    def delete_password(self, website):
        with self._connect() as connection:
            cursor = connection.cursor()
            cursor.execute('''DELETE FROM Passwords WHERE Website = ?''', (website,))
            connection.commit()
            return cursor.rowcount > 0

    # ------------------------------------------------------------------
    # توليد كلمة مرور
    # ------------------------------------------------------------------
    def generate_password(self):
        letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        nums = "1234567890"
        symbols = "-+=!@#$%^&*"

        password_chars = []
        password_chars += [choice(letters) for _ in range(randint(8, 12))]
        password_chars += [choice(nums) for _ in range(randint(3, 5))]
        password_chars += [choice(symbols) for _ in range(randint(3, 5))]

        shuffle(password_chars)
        return "".join(password_chars)

    @staticmethod
    def is_password_strong(password):
        """تحقق بسيط من قوة كلمة مرور مُدخلة يدوياً."""
        if len(password) < 8:
            return False
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        return has_upper and has_digit