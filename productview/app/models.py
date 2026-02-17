import psycopg2
from psycopg2.extras import DictCursor
from .config import Config

class Database:
    @staticmethod
    def get_connection():
        return psycopg2.connect(Config.DATABASE_URL, cursor_factory=DictCursor)

class Product:
    @staticmethod
    def get_by_id(product_id):
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT id, name, description, category, price, 
                       production_date, batch_number, template_type,
                       created_at, updated_at
                FROM products 
                WHERE id = %s
            """, (product_id,))
            
            product = cursor.fetchone()
            return dict(product) if product else None
            
        except Exception as e:
            print(f"Database error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()