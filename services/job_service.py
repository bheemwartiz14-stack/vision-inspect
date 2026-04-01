import sqlite3
from config.settings import DB_PATH

class JobService:

    def create_job(self, title, description, image, status, company_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO jobs (title, description, image_path, status, company_id)
        VALUES (?, ?, ?, ?, ?)
        """, (title, description, image, status, company_id))

        conn.commit()
        conn.close()

    def get_jobs(self, company_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM jobs WHERE company_id=?", (company_id,))
        data = cursor.fetchall()

        conn.close()
        return data

    def get_job_by_id(self, job_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jobs WHERE id=?", (job_id,))
        job = cursor.fetchone()
        conn.close()
        return job