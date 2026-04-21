from fastapi import FastAPI, Request, APIRouter, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app import db

router = APIRouter()
app = FastAPI(title="DataBass")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="pages")

@router.get("/assign-instrument", response_class=HTMLResponse)
def assign_instrument_page(request: Request):
    return templates.TemplateResponse(request, "assign_instrument.html")


@router.post("/assign-instrument", response_class=HTMLResponse)
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

@router.get("/instruments", response_class=HTMLResponse)
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