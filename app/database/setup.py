"""
Database Initialization Module
Handles the creation of the schema and seeding of mock data.
Uses Environment Variables for secure connection.
"""
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def init_db():
    """
    Connects to MySQL server, creates the MiBikeBusiness database, 
    defines the table schema, and inserts initial seed data.
    """
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS")
        )
        cursor = conn.cursor()
        
        # Schema Definition
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME')}")
        cursor.execute(f"USE {os.getenv('DB_NAME')}")

        tables = {
            "Tiers": "CREATE TABLE IF NOT EXISTS Tiers (TierID INT PRIMARY KEY, TierName VARCHAR(50), HourlyRate DECIMAL(5,2))",
            "Hubs": "CREATE TABLE IF NOT EXISTS Hubs (HubID INT PRIMARY KEY, HubName VARCHAR(50), Capacity INT)",
            "Members": "CREATE TABLE IF NOT EXISTS Members (MemberID INT PRIMARY KEY AUTO_INCREMENT, Name VARCHAR(100), TierID INT, FOREIGN KEY (TierID) REFERENCES Tiers(TierID))",
            "Bikes": "CREATE TABLE IF NOT EXISTS Bikes (SerialNum VARCHAR(10) PRIMARY KEY, Model VARCHAR(50), Status VARCHAR(20), HubID INT, FOREIGN KEY (HubID) REFERENCES Hubs(HubID))",
            "Rentals": "CREATE TABLE IF NOT EXISTS Rentals (RentalID INT PRIMARY KEY AUTO_INCREMENT, MemberID INT, SerialNum VARCHAR(10), StartTime DATETIME, EndTime DATETIME, FOREIGN KEY (MemberID) REFERENCES Members(MemberID), FOREIGN KEY (SerialNum) REFERENCES Bikes(SerialNum))"
        }

        for name, ddl in tables.items():
            cursor.execute(ddl)
            print(f"Table '{name}' verified/created.")

        # Seed Data (Idempotent using INSERT IGNORE)
        cursor.execute("INSERT IGNORE INTO Tiers VALUES (1, 'Standard', 5.00), (2, 'Premium', 10.00)")
        cursor.execute("INSERT IGNORE INTO Hubs VALUES (1, 'Downtown Central', 25), (2, 'North Campus', 15)")
        cursor.execute("INSERT IGNORE INTO Members (MemberID, Name, TierID) VALUES (1, 'Alice Jones', 2), (2, 'Bob Smith', 1)")
        cursor.execute("INSERT IGNORE INTO Bikes VALUES ('B001', 'Roadster', 'Available', 1), ('B002', 'Electric', 'Available', 2)")
        
        conn.commit()
        print("--- Database Setup Complete ---")
    except Exception as e:
        print(f"CRITICAL ERROR during DB Setup: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    init_db()
