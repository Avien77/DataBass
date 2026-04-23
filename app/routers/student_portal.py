from fastapi import FastAPI, Request, APIRouter, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app import db


router = APIRouter()
app = FastAPI(title="DataBass")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="pages")

@router.post("/student_portal") 
def student_portal(request: Request, email: str = Form(...)):
    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)
    try:
        # Singlular Student information
        cursor.execute("SELECT * FROM Student WHERE Stud_Email = %s", (email,))
        student = cursor.fetchone()

        if not student:
            return templates.TemplateResponse(request, "login.html", {"error": "Email not found."})

        stud_id = student["Stud_ID"]

        # Guardians
        cursor.execute("""
            SELECT g.* FROM Guardian g
            JOIN Student_Guardian sg ON g.Guardian_ID = sg.Guardian_ID
            WHERE sg.Stud_ID = %s
        """, (stud_id,))
        guardians = cursor.fetchall()

        # Uniform rentals
        cursor.execute("SELECT * FROM Student_Uniform_Rentals WHERE Stud_ID = %s", (stud_id,))
        uniform_rentals = cursor.fetchall()

        # Instrument rentals
        cursor.execute("SELECT * FROM Student_Instrument_Rentals WHERE Stud_ID = %s", (stud_id,))
        instrument_rentals = cursor.fetchall()

        return templates.TemplateResponse(request, "student_portal.html", {
            "student": student,
            "guardians": guardians,
            "uniform_rentals": uniform_rentals,
            "instrument_rentals": instrument_rentals
        })
    finally:
        cursor.close()
        conn.close()