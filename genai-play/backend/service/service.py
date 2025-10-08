from utils.db_util import get_db_connection_from_settings

class User:

    @staticmethod
    def fetch_by_id(user_id):
        """Fetch a specific user record from PostgreSQL database by user_id using db_util connection."""
        conn = get_db_connection_from_settings()
        cur = conn.cursor()
        cur.execute("SELECT id, name, age, gender FROM users WHERE id = %s;", (user_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            return {
                "id":row[0],
                "name":row[1],
                "age":row[2],
                "gender":row[3]
            }
        return None

class Portfolio:
    def __init__(self):
       pass

    @staticmethod
    def fetch_by_portfolio_id(user_id):
        """Fetch portfolio for a specific user_id from the portfolio table."""
        conn = get_db_connection_from_settings()
        cur = conn.cursor()
        cur.execute("""
            SELECT total_money, invested, isa_life_time, pension, cash_isa, stocks, GIA, balance
            FROM portfolio WHERE user_id = %s;
        """, (user_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            return {
                "total_money": row[0],
                "invested": row[1],
                "isa_life_time": row[2],
                "pension": row[3],
                "cash_isa": row[4],
                "stocks": row[5],
                "GIA": row[6],
                "balance": row[7]
            }
        return None

class Resources:
    def __init__(self):
        pass

    @staticmethod
    def fetch_categories():
        """Fetch all resource categories and their available content."""
        conn = get_db_connection_from_settings()
        cur = conn.cursor()
        cur.execute("SELECT category FROM resources;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        categories = []
        for row in rows:
            categories.append({
                "category": row[0]
            })
        return categories
    
    @staticmethod
    def fetch_by_category(category):
        """Fetch resources by category."""
        conn = get_db_connection_from_settings()
        cur = conn.cursor()
        cur.execute("SELECT available_content FROM resources WHERE category = %s;", (category,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            return {
                "category": category,
                "available_content": row[0]
            }
        return None