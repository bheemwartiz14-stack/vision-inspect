import sqlite3
from datetime import datetime
from config.settings import DB_PATH

class AuthService:

    def register(self, name, email, password, code, company):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT id, activation_code, activation_expiry 
        FROM companies WHERE register_id=?
        """, (company,))
        comp = cursor.fetchone()

        if not comp:
            return False, "Invalid Company ID"

        comp_id, db_code, expiry = comp

        if code != db_code:
            return False, "Invalid Activation Code"

        if datetime.now() > datetime.strptime(expiry, "%Y-%m-%d"):
            return False, "Activation Expired"

        cursor.execute("""
        INSERT INTO users (full_name, email, password, company_id)
        VALUES (?, ?, ?, ?)
        """, (name, email, password, comp_id))

        conn.commit()
        conn.close()
        return True, "Registered"

    def login(self, email, password, company):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT users.id, companies.id FROM users
        JOIN companies ON users.company_id = companies.id
        WHERE email=? AND password=? AND register_id=?
        """, (email, password, company))

        row = cursor.fetchone()
        conn.close()

        if not row:
            return False, None

        user_id, company_id = row
        return True, {"user_id": user_id, "company_id": company_id, "register_id": company}
