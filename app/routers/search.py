from fastapi import FastAPI, Request, APIRouter, Form
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