from fastapi import FastAPI, Request, APIRouter, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app import db

router = APIRouter()
app = FastAPI(title="DataBass")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="pages")

# TODO: 
@router.get("/rental", response_class=HTMLResponse)
def rental_page(request: Request):
    return templates.TemplateResponse(request, "rental.html")


@router.post("/rental", response_class=HTMLResponse)
def rental_lookup(request: Request, stud_id: str = Form(...)):
    # TODO: Remove Hardcoded values
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