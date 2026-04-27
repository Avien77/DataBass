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
            headers = ["Student ID", "First Name", "Last Name", "Grade", "Role"]
 
            if query:
                cursor.execute(
                    "SELECT Stud_ID, Stud_FName, Stud_LName, Stud_Grade, Stud_Role "
                    "FROM Student "
                    "WHERE CAST(Stud_ID AS CHAR) LIKE %s "
                    "OR Stud_FName LIKE %s "
                    "OR Stud_LName LIKE %s "
                    "OR Stud_Grade LIKE %s "
                    "OR Stud_Role LIKE %s",
                    (f"%{query}%",) * 5
                )
            else:
                cursor.execute(
                    "SELECT Stud_ID, Stud_FName, Stud_LName, Stud_Grade, Stud_Role "
                    "FROM Student"
                )
 
            rows = cursor.fetchall()
            results = [
                [
                    row["Stud_ID"],
                    row["Stud_FName"],
                    row["Stud_LName"],
                    row["Stud_Grade"] or "—",
                    row["Stud_Role"] or "—",
                ]
                for row in rows
            ]
 
        elif category == "guardians":
            headers = ["Guardian ID", "First Name", "Last Name", "Phone", "Email", "Student ID"]
 
            if query:
                cursor.execute(
                    "SELECT g.Guardian_ID, g.Guardian_FName, g.Guardian_LName, "
                    "g.Guardian_Phone, g.Guardian_Email, sg.Stud_ID "
                    "FROM Guardian g "
                    "LEFT JOIN Student_Guardian sg ON g.Guardian_ID = sg.Guardian_ID "
                    "WHERE CAST(g.Guardian_ID AS CHAR) LIKE %s "
                    "OR g.Guardian_FName LIKE %s "
                    "OR g.Guardian_LName LIKE %s "
                    "OR g.Guardian_Phone LIKE %s "
                    "OR g.Guardian_Email LIKE %s",
                    (f"%{query}%",) * 5
                )
            else:
                cursor.execute(
                    "SELECT g.Guardian_ID, g.Guardian_FName, g.Guardian_LName, "
                    "g.Guardian_Phone, g.Guardian_Email, sg.Stud_ID "
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
                    row["Guardian_Email"] or "—",
                    row["Stud_ID"] or "—",
                ]
                for row in rows
            ]
 
        elif category == "uniforms":
            headers = ["Uniform ID", "Type", "Role", "Size", "Status", "Student ID"]
 
            if query:
                cursor.execute(
                    "SELECT u.Uniform_ID, ut.Uniform_Type_Name, ut.Uniform_Role, "
                    "u.Uniform_Size, u.Uniform_Status, u.Stud_ID "
                    "FROM Uniform u "
                    "JOIN Uniform_Types ut ON u.Uniform_Type = ut.Uniform_Type_ID "
                    "WHERE CAST(u.Uniform_ID AS CHAR) LIKE %s "
                    "OR ut.Uniform_Type_Name LIKE %s "
                    "OR ut.Uniform_Role LIKE %s "
                    "OR u.Uniform_Size LIKE %s "
                    "OR u.Uniform_Status LIKE %s",
                    (f"%{query}%",) * 5
                )
            else:
                cursor.execute(
                    "SELECT u.Uniform_ID, ut.Uniform_Type_Name, ut.Uniform_Role, "
                    "u.Uniform_Size, u.Uniform_Status, u.Stud_ID "
                    "FROM Uniform u "
                    "JOIN Uniform_Types ut ON u.Uniform_Type = ut.Uniform_Type_ID"
                )
 
            rows = cursor.fetchall()
            results = [
                [
                    row["Uniform_ID"],
                    row["Uniform_Type_Name"] or "—",
                    row["Uniform_Role"] or "—",
                    row["Uniform_Size"] or "—",
                    row["Uniform_Status"] or "—",
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
