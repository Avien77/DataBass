import os
from mysql.connector import pooling
from dotenv import load_dotenv

load_dotenv()

# Initialize Connection Pool
# pooling prevents the overhead of opening/closing connections for every request.
db_pool = pooling.MySQLConnectionPool(
    pool_name="velocity_pool",
    pool_size=10,  # Max 10 simultaneous connections
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME")
)

def get_db_conn():
    """Retrieves a connection from the pre-warmed connection pool."""
    print("Connected to database")
    return db_pool.get_connection()