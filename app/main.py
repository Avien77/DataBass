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
            "message": f"Submitted for {stud_id}"
        }
    )


@app.get("/rental", response_class=HTMLResponse)
def rental_page(request: Request):
    return templates.TemplateResponse("rental.html", {"request": request})


@app.post("/rental", response_class=HTMLResponse)
def rental_lookup(request: Request, stud_id: str = Form(...)):
    fake_data = [
        {"item_type": "Uniform", "item_id": "U100", "status": "With Student"},
        {"item_type": "Instrument", "item_id": "I55", "status": "Returned"},
    ]

    return templates.TemplateResponse(
        "rental.html",
        {"request": request, "rentals": fake_data}
    )
