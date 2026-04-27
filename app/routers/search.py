from fastapi import FastAPI, Request, APIRouter
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
 
    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)
 
    try:
        if category == "students":
            headers = ["Student ID", "First Name", "Last Name", "Year", "Gender", "Phone", "Email"]
 
            if query:
                cursor.execute(
                    "SELECT Stud_ID, Stud_FName, Stud_LName, Year_ID, Stud_Gender, Stud_Phone, Stud_Email "
                    "FROM Student "
                    "WHERE CAST(Stud_ID AS CHAR) LIKE %s "
                    "OR Stud_FName LIKE %s "
                    "OR Stud_LName LIKE %s "
                    "OR Stud_Phone LIKE %s "
                    "OR Stud_Email LIKE %s",
                    (f"%{query}%",) * 5
                )
            else:
                cursor.execute(
                    "SELECT Stud_ID, Stud_FName, Stud_LName, Year_ID, Stud_Gender, Stud_Phone, Stud_Email "
                    "FROM Student"
                )
 
            year_map = {1: "Freshman", 2: "Sophomore", 3: "Junior", 4: "Senior"}
            rows = cursor.fetchall()
            results = [
                [
                    row["Stud_ID"],
                    row["Stud_FName"],
                    row["Stud_LName"],
                    year_map.get(row["Year_ID"], "Graduated"),
                    row["Stud_Gender"] or "—",
                    row["Stud_Phone"] or "—",
                    row["Stud_Email"] or "—",
                ]
                for row in rows
            ]
 
        elif category == "guardians":
            headers = ["Guardian ID", "First Name", "Last Name", "Phone", "Student ID"]
 
            if query:
                cursor.execute(
                    "SELECT g.Guardian_ID, g.Guardian_FName, g.Guardian_LName, "
                    "g.Guardian_Phone, sg.Stud_ID "
                    "FROM Guardian g "
                    "LEFT JOIN Student_Guardian sg ON g.Guardian_ID = sg.Guardian_ID "
                    "WHERE CAST(g.Guardian_ID AS CHAR) LIKE %s "
                    "OR g.Guardian_FName LIKE %s "
                    "OR g.Guardian_LName LIKE %s "
                    "OR g.Guardian_Phone LIKE %s",
                    (f"%{query}%",) * 4
                )
            else:
                cursor.execute(
                    "SELECT g.Guardian_ID, g.Guardian_FName, g.Guardian_LName, "
                    "g.Guardian_Phone, sg.Stud_ID "
                    "FROM Guardian g "
                    "LEFT JOIN Student_Guardian sg ON g.Guardian_ID = sg.Guardian_ID"
                )
 
            rows = cursor.fetchall()
            results = [
                [
                    row["Guardian_ID"],
                    row["Guardian_FName"],
                    row["Guardian_LName"],
                    row["Guardian_Phone"] or "—",
                    row["Stud_ID"] or "—",
                ]
                for row in rows
            ]
 
        elif category == "uniforms":
            headers = ["Uniform ID", "Role", "Chest", "Arms", "Hips", "Waist", "Inseam", "Gloves", "Student ID"]
 
            if query:
                cursor.execute(
                    "SELECT u.Uniform_ID, r.Role_Name, u.Uniform_Chest, u.Uniform_Arms, "
                    "u.Uniform_Hips, u.Uniform_Waist, u.Uniform_Inseam, u.Uniform_Gloves, "
                    "sur.Stud_ID "
                    "FROM Uniform u "
                    "JOIN Role r ON u.Role_ID = r.Role_ID "
                    "LEFT JOIN Student_Uniform_Rentals sur ON u.Uniform_ID = sur.Uniform_ID "
                    "AND sur.Unif_Rental_End_Date IS NULL "
                    "WHERE CAST(u.Uniform_ID AS CHAR) LIKE %s "
                    "OR r.Role_Name LIKE %s",
                    (f"%{query}%",) * 2
                )
            else:
                cursor.execute(
                    "SELECT u.Uniform_ID, r.Role_Name, u.Uniform_Chest, u.Uniform_Arms, "
                    "u.Uniform_Hips, u.Uniform_Waist, u.Uniform_Inseam, u.Uniform_Gloves, "
                    "sur.Stud_ID "
                    "FROM Uniform u "
                    "JOIN Role r ON u.Role_ID = r.Role_ID "
                    "LEFT JOIN Student_Uniform_Rentals sur ON u.Uniform_ID = sur.Uniform_ID "
                    "AND sur.Unif_Rental_End_Date IS NULL"
                )
 
            rows = cursor.fetchall()
            results = [
                [
                    row["Uniform_ID"],
                    row["Role_Name"] or "—",  # column is Role_Name in Role table
                    row["Uniform_Chest"] or "—",
                    row["Uniform_Arms"] or "—",
                    row["Uniform_Hips"] or "—",
                    row["Uniform_Waist"] or "—",
                    row["Uniform_Inseam"] or "—",
                    row["Uniform_Gloves"] or "—",
                    row["Stud_ID"] or "—",
                ]
                for row in rows
            ]
 
        elif category == "instruments":
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
                    "WHERE CAST(i.Instrument_ID AS CHAR) LIKE %s "
                    "OR t.Instr_Type_Name LIKE %s "
                    "OR s.Stud_FName LIKE %s "
                    "OR s.Stud_LName LIKE %s",
                    (f"%{query}%",) * 4
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
                    "Active" if row["Stud_ID"] and not row["Instr_Rental_End_Date"]
                    else ("Returned" if row["Instr_Rental_End_Date"] else "Never Rented"),
                ]
                for row in rows
            ]
 
        elif category == "rentals":
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
                    "OR s.Stud_FName LIKE %s "
                    "OR s.Stud_LName LIKE %s "
                    "OR t.Instr_Type_Name LIKE %s",
                    (f"%{query}%",) * 4
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
                    row["Instr_Rental_Start_Date"] or "—",
                    row["Instr_Rental_End_Date"] or "—",
                    row["Instr_Start_Condition"] or "—",
                    row["Instr_End_Condition"] or "—",
                    "Active" if not row["Instr_Rental_End_Date"] else "Returned",
                ]
                for row in rows
            ]
 
    except Exception as e:
        print(f"Search error: {e}")
    finally:
        cursor.close()
        conn.close()
 
    return templates.TemplateResponse(
        request,
        "search.html",
        {
            "request": request,
            "headers": headers,
            "results": results,
            "category": category,
            "query": query,
        }
    )
