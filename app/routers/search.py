from fastapi import FastAPI, Request, APIRouter, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app import db

router = APIRouter()
app = FastAPI(title="DataBass")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="pages")

@router.get("/search", response_class=HTMLResponse)
def search_page(request: Request, category: str = "", query: str = ""):
    headers = []
    results = []

    if category == "rentals":
        conn = db.get_db_conn()
        cursor = conn.cursor(dictionary=True)

        try:
            headers = ["Student ID", "Student Name", "Instrument Type", "Start Date", "End Date", "Start Condition", "End Condition", "Status"]

            if query:
                cursor.execute(
                    "SELECT r.Stud_ID, s.Stud_FName, s.Stud_LName, t.Instr_Type_Name, "
                    "r.Instr_Rental_Start_Date, r.Instr_Rental_End_Date, "
                    "r.Instr_Start_Condition, r.Instr_End_Condition "
                    "FROM Student_Instrument_Rentals r "
                    "JOIN Student s ON r.Stud_ID = s.Stud_ID "
                    "JOIN Instrument i ON r.Instrument_ID = i.Instrument_ID "
                    "JOIN Instrument_Types t ON i.Instrument_Type = t.Instr_Type_ID "
                    "WHERE CAST(r.Stud_ID AS CHAR) LIKE %s "
                    "OR s.Stud_FName LIKE %s OR s.Stud_LName LIKE %s "
                    "OR t.Instr_Type_Name LIKE %s",
                    (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%")
                )
            else:
                cursor.execute(
                    "SELECT r.Stud_ID, s.Stud_FName, s.Stud_LName, t.Instr_Type_Name, "
                    "r.Instr_Rental_Start_Date, r.Instr_Rental_End_Date, "
                    "r.Instr_Start_Condition, r.Instr_End_Condition "
                    "FROM Student_Instrument_Rentals r "
                    "JOIN Student s ON r.Stud_ID = s.Stud_ID "
                    "JOIN Instrument i ON r.Instrument_ID = i.Instrument_ID "
                    "JOIN Instrument_Types t ON i.Instrument_Type = t.Instr_Type_ID"
                )

            rows = cursor.fetchall()
            results = [
                [
                    row["Stud_ID"],
                    f"{row['Stud_FName']} {row['Stud_LName']}",
                    row["Instr_Type_Name"],
                    row["Instr_Rental_Start_Date"],
                    row["Instr_Rental_End_Date"] or "—",
                    row["Instr_Start_Condition"] or "—",
                    row["Instr_End_Condition"] or "—",
                    "Active" if not row["Instr_Rental_End_Date"] else "Returned"
                ]
                for row in rows
            ]
        except Exception as e:
            print(f"Search error: {e}")
        finally:
            cursor.close()
            conn.close()

    elif category == "students":
        headers = ["Student ID", "First Name", "Last Name", "Year", "Role"]
        results = [
            ["S100", "Nate", "Oberdier", "Junior", "Regular"],
            ["S101", "Alex", "Smith", "Senior", "Percussion"]
        ]
    elif category == "guardians":
        headers = ["Guardian ID", "First Name", "Last Name", "Phone"]
        results = [
            ["G100", "John", "Oberdier", "555-111-2222"],
            ["G101", "Mary", "Smith", "555-333-4444"]
        ]
    elif category == "uniforms":
        headers = ["Uniform ID", "Type", "Role", "Size", "Status"]
        results = [
            ["U100", "Jacket", "Regular", "M", "With Student"],
            ["U101", "Pants", "Regular", "32", "On Shelf"]
        ]
    elif category == "instruments":
        conn = db.get_db_conn()
        cursor = conn.cursor(dictionary=True)

        try:
            headers = ["Instrument ID", "Type", "Rented To", "Student ID", "Rented Out Date", "Return Date", "Status"]

            if query:
                cursor.execute(
                    "SELECT i.Instrument_ID, t.Instr_Type_Name, "
                    "s.Stud_ID, s.Stud_FName, s.Stud_LName, "
                    "r.Instr_Rental_Start_Date, r.Instr_Rental_End_Date "
                    "FROM Instrument i "
                    "JOIN Instrument_Types t ON i.Instrument_Type = t.Instr_Type_ID "
                    "LEFT JOIN Student_Instrument_Rentals r ON i.Instrument_ID = r.Instrument_ID "
                    "LEFT JOIN Student s ON r.Stud_ID = s.Stud_ID "
                    "WHERE CAST(i.Instrument_ID AS CHAR) LIKE %s OR t.Instr_Type_Name LIKE %s "
                    "OR s.Stud_FName LIKE %s OR s.Stud_LName LIKE %s",
                    (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%")
                )
            else:
                cursor.execute(
                    "SELECT i.Instrument_ID, t.Instr_Type_Name, "
                    "s.Stud_ID, s.Stud_FName, s.Stud_LName, "
                    "r.Instr_Rental_Start_Date, r.Instr_Rental_End_Date "
                    "FROM Instrument i "
                    "JOIN Instrument_Types t ON i.Instrument_Type = t.Instr_Type_ID "
                    "LEFT JOIN Student_Instrument_Rentals r ON i.Instrument_ID = r.Instrument_ID "
                    "LEFT JOIN Student s ON r.Stud_ID = s.Stud_ID"
                )

            rows = cursor.fetchall()
            results = [
                [
                    row["Instrument_ID"],
                    row["Instr_Type_Name"],
                    f"{row['Stud_FName']} {row['Stud_LName']}" if row["Stud_ID"] else "—",
                    row["Stud_ID"] or "—",
                    row["Instr_Rental_Start_Date"] or "—",
                    row["Instr_Rental_End_Date"] or "—",
                    "Active" if row["Stud_ID"] and not row["Instr_Rental_End_Date"] else ("Returned" if row["Instr_Rental_End_Date"] else "Never Rented")
                ]
                for row in rows
            ]
        except Exception as e:
            print(f"Search error: {e}")
        finally:
            cursor.close()
            conn.close()

            
    if query and results and category != "rentals":
        q = query.lower()
        results = [
            row for row in results
            if any(q in str(value).lower() for value in row)
        ]

    return templates.TemplateResponse(
        request,
        "search.html",
        {
            "request": request,
            "headers": headers,
            "results": results
        }
    )