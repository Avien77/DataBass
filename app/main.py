import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from mysql.connector import pooling
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="DataBass")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="pages")

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

# we probably shouldn't need this if we follow good practices
year_to_id = { 
        "Freshman": 1, 
        "Sophomore": 2, 
        "Junior": 3,
        "Senior": 4
    }

def get_db_conn():
    """Retrieves a connection from the pre-warmed connection pool."""
    print("Connected to database")
    return db_pool.get_connection()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)

    try:

        return templates.TemplateResponse(request, "dashboard.html")
    finally:
        cursor.close()
        conn.close() # Returns connection to pool

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(request, "dashboard.html")


@app.get("/measurements", response_class=HTMLResponse)
def measurements_page(request: Request):
    return templates.TemplateResponse(request, "measurements.html")


@app.post("/measurements", response_class=HTMLResponse)
def submit_measurements(
    request: Request,
    stud_id: str = Form(...),
    chest: str = Form(""),
    arms: str = Form(""),
    hips: str = Form(""),
    waist: str = Form(""),
    inseam: str = Form(""),
    gloves: str = Form(""),
    instrument: str = Form(""),
    role: str = Form(""),
    student_year: str = Form("")
):
    return templates.TemplateResponse(
        request,
        "measurements.html",
        {
            "request": request,
            "message": f"Measurements submitted for student {stud_id}"
        }
    )


@app.get("/rental", response_class=HTMLResponse)
def rental_page(request: Request):
    return templates.TemplateResponse(request, "rental.html")


@app.post("/rental", response_class=HTMLResponse)
def rental_lookup(request: Request, stud_id: str = Form(...)):
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
        "rental.html",
        {
            "request": request,
            "rentals": rentals
        }
    )


@app.get("/add-student", response_class=HTMLResponse)
def add_student_page(request: Request):
    return templates.TemplateResponse(request, "add_student.html")


@app.post("/add-student")
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
    conn = get_db_conn()
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
        return templates.TemplateResponse(
            request,
            "add_student.html",
            {"request": request, "message": f"Student {first_name} {last_name} added successfully"},
            status_code=200
        )
    return templates.TemplateResponse(
        request,
        "add_student.html",
        {"request": request, "error": f"Failed to add student: {error_message}"},
        status_code=500
    )


@app.get("/edit-student", response_class=HTMLResponse)
def edit_student_page(request: Request):
    return templates.TemplateResponse(
        request,
        "edit_student.html",
        {
            "request": request,
            "student": None
        }
    )


@app.post("/edit-student", response_class=HTMLResponse)
def edit_student_submit(
    request: Request,
    stud_id: str = Form(...),
    first_name: str = Form(""),
    last_name: str = Form(""),
    phone: str = Form(""),
    email: str = Form(""),
    gender: str = Form(""),
    student_year: str = Form(""),
    role: str = Form("")
):
    student = {
        "stud_id": stud_id,
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone,
        "email": email,
        "gender": gender,
        "student_year": student_year,
        "role": role
    }

    return templates.TemplateResponse(
        request,
        "edit_student.html",
        {
            "request": request,
            "student": student,
            "message": f"Student {stud_id} updated successfully"
        }
    )


@app.get("/student-details", response_class=HTMLResponse)
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


@app.get("/add-guardian", response_class=HTMLResponse)
def add_guardian_page(request: Request):
    return templates.TemplateResponse(request, "add_guardian.html")


@app.post("/add-guardian", response_class=HTMLResponse)
def add_guardian_submit(
    request: Request,
    guard_id: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    phone: str = Form(...),
):
    
    conn = get_db_conn()
    cursor = conn.cursor()

    success = False
    error_message = None

    try:
        cursor.execute("INSERT INTO Guardian (Guardian_ID, Guardian_FName, Guardian_LName, Guardian_Phone) VALUES" \
        "(%s, %s, %s, %s)",
        (guard_id, first_name, last_name, phone))
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
        return templates.TemplateResponse(
            request,
            "add_guardian.html",
            {"request": request, "message": f"Guardian {first_name} {last_name} added successfully"},
            status_code=200
        )
    return templates.TemplateResponse(
        request,
        "add_guardian.html",
        {"request": request, "error": f"Failed to add guardian: {error_message}"},
        status_code=500
    )


@app.get("/link-guardian", response_class=HTMLResponse)
def link_guardian_page(request: Request):
    return templates.TemplateResponse(request, "link_guardian.html")


@app.post("/link-guardian", response_class=HTMLResponse)
def link_guardian_submit(
    request: Request,
    stud_id: str = Form(...),
    guard_id: str = Form(...)
):
    return templates.TemplateResponse(
        request,
        "link_guardian.html",
        {
            "request": request,
            "message": f"Guardian {guard_id} linked to student {stud_id}"
        }
    )


@app.get("/assign-uniform", response_class=HTMLResponse)
def assign_uniform_page(request: Request):
    return templates.TemplateResponse(request, "assign_uniform.html")


@app.post("/assign-uniform", response_class=HTMLResponse)
def assign_uniform_submit(
    request: Request,
    stud_id: str = Form(...),
    staff_id: str = Form(...),
    uniform_type: str = Form(...),
    uniform_id: str = Form(...),
    start_condition: str = Form(...),
    rental_start_date: str = Form(...)
):
    return templates.TemplateResponse(
        request,
        "assign_uniform.html",
        {
            "request": request,
            "message": f"{uniform_type} {uniform_id} assigned to student {stud_id}"
        }
    )


@app.get("/assign-instrument", response_class=HTMLResponse)
def assign_instrument_page(request: Request):
    return templates.TemplateResponse(request, "assign_instrument.html")


@app.post("/assign-instrument", response_class=HTMLResponse)
def assign_instrument_submit(
    request: Request,
    stud_id: str = Form(...),
    staff_id: str = Form(...),
    instrument_id: str = Form(...),
    start_condition: str = Form(...),
    rental_start_date: str = Form(...)
):
    return templates.TemplateResponse(
        request,
        "assign_instrument.html",
        {
            "request": request,
            "message": f"Instrument {instrument_id} assigned to student {stud_id}"
        }
    )


@app.get("/return-item", response_class=HTMLResponse)
def return_item_page(request: Request):
    return templates.TemplateResponse(request, "return_item.html")


@app.post("/return-item", response_class=HTMLResponse)
def return_item_submit(
    request: Request,
    stud_id: str = Form(...),
    staff_id: str = Form(...),
    item_type: str = Form(...),
    item_id: str = Form(...),
    end_condition: str = Form(...),
    return_date: str = Form(...)
):
    return templates.TemplateResponse(
        request,
        "return_item.html",
        {
            "request": request,
            "message": f"{item_type} {item_id} returned for student {stud_id}"
        }
    )


@app.get("/uniforms", response_class=HTMLResponse)
def uniforms_page(request: Request, query: str = ""):
    uniforms = [
        {
            "uniform_id": "U100",
            "uniform_type": "Jacket",
            "role": "Regular",
            "size": "M",
            "status": "With Student"
        },
        {
            "uniform_id": "U101",
            "uniform_type": "Pants",
            "role": "Regular",
            "size": "32",
            "status": "On Shelf"
        }
    ]

    if query:
        q = query.lower()
        uniforms = [
            u for u in uniforms
            if q in u["uniform_id"].lower()
            or q in u["uniform_type"].lower()
            or q in u["role"].lower()
            or q in u["size"].lower()
            or q in u["status"].lower()
        ]

    return templates.TemplateResponse(
        request,
        "uniforms.html",
        {
            "request": request,
            "uniforms": uniforms
        }
    )


@app.get("/instruments", response_class=HTMLResponse)
def instruments_page(request: Request, query: str = ""):
    instruments = [
        {
            "instrument_id": "I55",
            "instrument_type": "Trumpet",
            "brand": "Yamaha",
            "asset_id": "A-1001",
            "status": "With Student"
        },
        {
            "instrument_id": "I56",
            "instrument_type": "Flute",
            "brand": "Pearl",
            "asset_id": "A-1002",
            "status": "On Shelf"
        }
    ]

    if query:
        q = query.lower()
        instruments = [
            i for i in instruments
            if q in i["instrument_id"].lower()
            or q in i["instrument_type"].lower()
            or q in i["brand"].lower()
            or q in i["asset_id"].lower()
            or q in i["status"].lower()
        ]

    return templates.TemplateResponse(
        request,
        "instruments.html",
        {
            "request": request,
            "instruments": instruments
        }
    )


@app.get("/search", response_class=HTMLResponse)
def search_page(request: Request, category: str = "", query: str = ""):
    headers = []
    results = []

    if category == "students":
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
        headers = ["Instrument ID", "Type", "Brand", "Asset ID", "Status"]
        results = [
            ["I55", "Trumpet", "Yamaha", "A-1001", "With Student"],
            ["I56", "Flute", "Pearl", "A-1002", "On Shelf"]
        ]
    elif category == "rentals":
        headers = ["Student ID", "Item Type", "Item ID", "Status"]
        results = [
            ["S100", "Uniform", "U100", "With Student"],
            ["S100", "Instrument", "I55", "Returned"]
        ]

    if query and results:
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
