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
            "Student": "CREATE TABLE IF NOT EXISTS Student (Stud_ID INT PRIMARY KEY, Stud_FName VARCHAR(50), Stud_LName VARCHAR(50), Stud_Phone VARCHAR(15), Year_ID INT, Stud_Gender VARCHAR(10), Stud_Email VARCHAR(100))",
            "Uniform": "CREATE TABLE IF NOT EXISTS Uniform (Uniform_ID INT PRIMARY KEY AUTO_INCREMENT, Role_ID INT, Uniform_Chest DECIMAL(5,2), Uniform_Arms DECIMAL(5,2), Uniform_Hips DECIMAL(5,2),Uniform_Waist DECIMAL(5,2), Uniform_Inseam DECIMAL(5,2), Uniform_Gloves VARCHAR(10))",
            "Instrument": "CREATE TABLE IF NOT EXISTS Instrument (Instrument_ID INT PRIMARY KEY, Instrument_Type INT, Instrument_Brand VARCHAR(100))",
            "Instrument_Types": "CREATE TABLE IF NOT EXISTS Instrument_Types (Instr_Type_ID INT PRIMARY KEY AUTO_INCREMENT, Instr_Type_Name VARCHAR(50), UNIQUE (Instr_Type_Name))",
            "Role": "CREATE TABLE IF NOT EXISTS Role (Role_ID INT PRIMARY KEY, Role_Name VARCHAR(50), UNIQUE (Role_Name))",
            "Guardian": "CREATE TABLE IF NOT EXISTS Guardian (Guardian_ID INT PRIMARY KEY, Guardian_FName VARCHAR(50), Guardian_LName VARCHAR(50), Guardian_Phone VARCHAR(15))",
            "Student_Role": "CREATE TABLE IF NOT EXISTS Student_Role (Stud_ID INT, Role_ID INT, PRIMARY KEY (Stud_ID, Role_ID), FOREIGN KEY (Stud_ID) REFERENCES Student(Stud_ID), FOREIGN KEY (Role_ID) REFERENCES Role(Role_ID))",
            "Student_Uniform_Rentals": "CREATE TABLE IF NOT EXISTS Student_Uniform_Rentals (Uniform_Rental_ID INT PRIMARY KEY AUTO_INCREMENT, Stud_ID int, Uniform_ID INT, Unif_Rental_Start_Date DATE, Unif_Rental_End_Date DATE, Unif_Start_Condition VARCHAR(100), Unif_End_Condition VARCHAR(100), FOREIGN KEY (Stud_ID) REFERENCES Student(Stud_ID), FOREIGN KEY (Uniform_ID) REFERENCES Uniform(Uniform_ID))",
            "Student_Instrument_Rentals": "CREATE TABLE IF NOT EXISTS Student_Instrument_Rentals (Instr_Rental_ID INT PRIMARY KEY AUTO_INCREMENT, Stud_ID INT, Instrument_ID INT, Instr_Rental_Start_Date DATE, Instr_Rental_End_Date DATE, Instr_Start_Condition VARCHAR(100), Instr_End_Condition VARCHAR(100), FOREIGN KEY (Stud_ID) REFERENCES Student(Stud_ID), FOREIGN KEY (Instrument_ID) REFERENCES Instrument(Instrument_ID))",
            "Student_Guardian": "CREATE TABLE IF NOT EXISTS Student_Guardian (Stud_ID INT, Guardian_ID INT, PRIMARY KEY (Stud_ID, Guardian_ID), FOREIGN KEY (Stud_ID) REFERENCES Student(Stud_ID), FOREIGN KEY (Guardian_ID) REFERENCES Guardian(Guardian_ID))"
        }

        for name, ddl in tables.items():
            cursor.execute(ddl)
            print(f"Table '{name}' verified/created.")
        
        conn.commit()
        print("--- Database Setup Complete ---")
    except Exception as e:
        print(f"CRITICAL ERROR during DB Setup: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected(): #type: ignore
            cursor.close() #type: ignore
            conn.close() #type: ignore

if __name__ == "__main__":
    init_db()
