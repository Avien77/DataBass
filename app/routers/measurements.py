from fastapi import FastAPI, Request, APIRouter, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app import db

router = APIRouter()
app = FastAPI(title="DataBass")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="pages")


@router.get("/measurements", response_class=HTMLResponse)
def measurements_page(request: Request):
    return templates.TemplateResponse(request, "measurements.html")


@router.post("/measurements", response_class=HTMLResponse)
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
