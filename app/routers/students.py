from fastapi import FastAPI, Request, APIRouter, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app import db

router = APIRouter()
app = FastAPI(title="DataBass")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="pages")

# we probably shouldn't need this if we follow good practices
year_to_id = {
        "Freshman": 1,
        "Sophomore": 2,
        "Junior": 3,
        "Senior": 4
    }

id_to_year = {v: k for k, v in year_to_id.items()}

@router.get("/student-list", response_class=HTMLResponse)
def add_student_list_page(request: Request):

    # get connection/cursor
    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)

    success = False
    error_message = None

    try:
        cursor.execute("SELECT * FROM STUDENT")
        students = cursor.fetchall()
        print(students)
        success=True
    except Exception as e:
        error_message = str(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    if success:
        return templates.TemplateResponse(
            request=request, 
            name="student_list.html",
            context={"students": students}, #type: ignore
            status_code=200
        )
    return templates.TemplateResponse(
        request=request,
        name="student_list.html",
        status_code=500
    )

@router.post("/search-student")
def search_student(
    request: Request,
    stud_fname: str | None = Form(None)
):
    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)

    success = False
    error_message = None

    # default, fetch all
    if not stud_fname:
        try:
            cursor.execute("SELECT * FROM Student")
            students = cursor.fetchall()
            success = True
        except Exception as e:
            error_message = str(e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
    else:
        try:
            cursor.execute("SELECT * FROM Student WHERE Stud_FName LIKE %s", (f"%{stud_fname}%",))
            students = cursor.fetchall()
            success = True
        except Exception as e:
            error_message = str(e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()


    if success:
        return templates.TemplateResponse(
            request,
            "student_list.html",
            {"students": students}, # type: ignore
            status_code=200
        )
    return templates.TemplateResponse(
            request,
            "student_list.html",
            status_code=500
    )

@router.get("/add-student", response_class=HTMLResponse)
def add_student_page(request: Request):
    return templates.TemplateResponse(request, "add_student.html")


@router.post("/add-student")
def add_student_submit(
    request: Request,
    stud_id: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    phone: str = Form(""),
    email: str = Form(""),
    gender: str = Form(""),
    student_year: str = Form(...),
):
    conn = db.get_db_conn()
    cursor = conn.cursor()

    success = False
    error_message = None

    yearId = year_to_id[student_year]

    try:
        cursor.execute("INSERT INTO Student (Stud_ID, Stud_FName, Stud_LName, Stud_Phone, Year_ID, Stud_Gender, Stud_Email) " \
        "VALUES (%s, %s, %s, %s, %s, %s, %s)", 
        (stud_id, first_name, last_name, phone, yearId, gender, email))
        conn.commit()
        success = True
    except Exception as e:
        conn.rollback()
        error_message = str(e)
        print(f"Transaction Failed: {e}")
    finally:
        cursor.close()
        conn.close()

    if success:
        return RedirectResponse(url="/student-list", status_code=303)
    return templates.TemplateResponse(
        request,
        "add_student.html",
        {"request": request, "error": f"Failed to add student: {error_message}"},
        status_code=500
    )

@router.get("/edit-student/{id}", response_class=HTMLResponse)
def edit_student_page(request: Request, id: str):
    conn = db.get_db_conn()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM Student WHERE Stud_ID = %s", (id,))
        student = cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

    if not student:
        return RedirectResponse(url="/student-list", status_code=303)

    student["Year_Name"] = id_to_year.get(student["Year_ID"], "")
    return templates.TemplateResponse(request, "add_student.html", {"student": student})


@router.post("/edit-student/{id}")
def edit_student_submit(
    request: Request,
    id: str,
    first_name: str = Form(...),
    last_name: str = Form(...),
    phone: str = Form(""),
    email: str = Form(""),
    gender: str = Form(""),
    student_year: str = Form(...),
):
    conn = db.get_db_conn()
    cursor = conn.cursor()

    success = False
    error_message = None
    yearId = year_to_id[student_year]

    try:
        cursor.execute(
            "UPDATE Student SET Stud_FName=%s, Stud_LName=%s, Stud_Phone=%s, Year_ID=%s, Stud_Gender=%s, Stud_Email=%s WHERE Stud_ID=%s",
            (first_name, last_name, phone, yearId, gender, email, id)
        )
        conn.commit()
        success = True
    except Exception as e:
        conn.rollback()
        error_message = str(e)
        print(f"Transaction Failed: {e}")
    finally:
        cursor.close()
        conn.close()

    if success:
        return RedirectResponse(url="/student-list", status_code=303)
    return templates.TemplateResponse(
        request,
        "add_student.html",
        {"student": {"Stud_ID": id}, "error": f"Failed to update student: {error_message}"},
        status_code=500
    )

@router.get("/student-details", response_class=HTMLResponse)
def student_details_page(request: Request, stud_id: str = ""):
    student = None
    guardians = []
    rentals = []

    if stud_id:
        student = {
            "stud_id": stud_id,
            "first_name": "Nate",
            "last_name": "Oberdier",
            "phone": "555-123-4567",
            "email": "student@example.com",
            "gender": "Male",
            "student_year": "Junior",
            "role": "Regular"
        }

        guardians = [
            {
                "guard_id": "G100",
                "first_name": "John",
                "last_name": "Oberdier",
                "phone": "555-111-2222"
            }
        ]

        rentals = [
            {
                "item_type": "Uniform",
                "item_id": "U100",
                "status": "With Student",
                "start_date": "2026-03-01",
                "end_date": ""
            },
            {
                "item_type": "Instrument",
                "item_id": "I55",
                "status": "Returned",
                "start_date": "2025-10-01",
                "end_date": "2026-01-10"
            }
        ]

    return templates.TemplateResponse(
        request,
        "student_details.html",
        {
            "request": request,
            "student": student,
            "guardians": guardians,
            "rentals": rentals
        }
    )
