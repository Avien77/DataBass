from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="DataBass")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="pages")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/measurements", response_class=HTMLResponse)
def measurements_page(request: Request):
    return templates.TemplateResponse("measurements.html", {"request": request})


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
        "measurements.html",
        {
            "request": request,
            "message": f"Measurements submitted for student {stud_id}"
        }
    )


@app.get("/rental", response_class=HTMLResponse)
def rental_page(request: Request):
    return templates.TemplateResponse("rental.html", {"request": request})


@app.post("/rental", response_class=HTMLResponse)
def rental_lookup(request: Request, stud_id: str = Form(...)):
    rentals = [
        {
            "item_type": "Uniform",
            "item_id": "U100",
            "status": "With Student"
        },
        {
            "item_type": "Instrument",
            "item_id": "I55",
            "status": "Returned"
        }
    ]

    return templates.TemplateResponse(
        "rental.html",
        {
            "request": request,
            "rentals": rentals
        }
    )


@app.get("/add-student", response_class=HTMLResponse)
def add_student_page(request: Request):
    return templates.TemplateResponse("add_student.html", {"request": request})


@app.post("/add-student", response_class=HTMLResponse)
def add_student_submit(
    request: Request,
    stud_id: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    phone: str = Form(""),
    email: str = Form(""),
    gender: str = Form(""),
    student_year: str = Form(...),
    role: str = Form("")
):
    return templates.TemplateResponse(
        "add_student.html",
        {
            "request": request,
            "message": f"Student {first_name} {last_name} added successfully"
        }
    )


@app.get("/assign-uniform", response_class=HTMLResponse)
def assign_uniform_page(request: Request):
    return templates.TemplateResponse("assign_uniform.html", {"request": request})


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
        "assign_uniform.html",
        {
            "request": request,
            "message": f"{uniform_type} {uniform_id} assigned to student {stud_id}"
        }
    )


@app.get("/return-item", response_class=HTMLResponse)
def return_item_page(request: Request):
    return templates.TemplateResponse("return_item.html", {"request": request})


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
        "return_item.html",
        {
            "request": request,
            "message": f"{item_type} {item_id} returned for student {stud_id}"
        }
    )
