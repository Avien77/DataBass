from fastapi import FastAPI, Request, APIRouter, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app import db

router = APIRouter()
app = FastAPI(title="DataBass")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="pages")


@router.get("/assign-uniform", response_class=HTMLResponse)
def assign_uniform_page(request: Request):
    return templates.TemplateResponse(request, "assign_uniform.html")


@router.post("/assign-uniform", response_class=HTMLResponse)
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



@router.get("/uniforms", response_class=HTMLResponse)
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