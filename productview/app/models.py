import psycopg2
from psycopg2.extras import DictCursor
from .config import Config
import logging
logger = logging.getLogger(__name__)

class Database:
    @staticmethod
    def get_connection():
        return psycopg2.connect(Config.DATABASE_URL, cursor_factory=DictCursor)

class Item:
    @staticmethod
    def get_by_id(item_id):
        conn = Database.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, name, description, category, price, 
                       production_date, batch_number, template_type,
                       image, created_at, updated_at
                FROM items 
                WHERE id = %s
            """, (item_id,))
            
            item = cursor.fetchone()
            return dict(item) if item else None
            
        except Exception as e:
            print(f"Database error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

class CodesTypes:
    @staticmethod
    def get_types():
        conn = Database.get_connection()
        logger.info('Connection to DB:' + str(conn))
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, ref_table, pattern, model, model_field, source, lastmodified
                FROM index 
            """)             
            codestypes = cursor.fetchall()
            return codestypes if codestypes else None
        except Exception as e:
            print(f"Database error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    indexes = get_types()