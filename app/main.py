"""
Velocity Ride Share - Main Application Logic
Uses FastAPI for routing, Jinja2 for UI rendering, 
and MySQL Connection Pooling for high-performance database access.
"""
import os
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from mysql.connector import pooling
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

app = FastAPI(title="Velocity Ride Share API")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

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
    return db_pool.get_connection()

@app.get("/")
def dashboard(request: Request):
    """
    Renders the main Management Dashboard for Alice.
    Fetches live Hub capacities and Active Rental lists.
    """
    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)
    try:
        # Business Logic: Fetch current status of all Hubs
        cursor.execute("SELECT * FROM Hubs")
        hubs = cursor.fetchall()
        
        # Business Logic: Join Members & Rentals to show who is currently riding
        query = "SELECT R.RentalID, M.Name as MemberName, R.SerialNum, R.StartTime FROM Rentals R JOIN Members M ON R.MemberID = M.MemberID WHERE R.EndTime IS NULL"
        cursor.execute(query)
        active_rentals = cursor.fetchall()

        return templates.TemplateResponse(
            request=request, 
            name="dashboard.html", 
            context={"hubs": hubs, "active_rentals": active_rentals}
        )
    finally:
        cursor.close()
        conn.close() # Returns connection to pool

@app.post("/checkout")
def checkout(member_id: int = Form(...), serial_num: str = Form(...)):
    """
    Executes an Atomic Transaction for Bike Checkouts.
    1. Creates a new Rental record.
    2. Updates Bike status to 'In-Use' and clears its Hub location.
    """
    conn = get_db_conn()
    cursor = conn.cursor()
    try:
        # Start Transaction (ACID Compliance)
        cursor.execute("INSERT INTO Rentals (MemberID, SerialNum, StartTime) VALUES (%s, %s, NOW())", (member_id, serial_num))
        cursor.execute("UPDATE Bikes SET Status = 'In-Use', HubID = NULL WHERE SerialNum = %s", (serial_num,))
        conn.commit()
    except Exception as e:
        conn.rollback() # Cancel all changes if any part fails
        print(f"Transaction Failed: {e}")
    finally:
        cursor.close()
        conn.close()
    return RedirectResponse(url="/", status_code=303)
