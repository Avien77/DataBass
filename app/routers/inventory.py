from fastapi import FastAPI, Request, APIRouter, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app import db

router = APIRouter()
app = FastAPI(title="DataBass")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="pages")

@router.get("/return-item", response_class=HTMLResponse)
def return_item_page(request: Request):
    return templates.TemplateResponse(request, "return_item.html")


@router.post("/return-item", response_class=HTMLResponse)
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

