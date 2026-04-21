from fastapi import FastAPI, Request, APIRouter, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app import db

router = APIRouter()
app = FastAPI(title="DataBass")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="pages")

@router.get("/add-guardian", response_class=HTMLResponse)
def add_guardian_page(request: Request):
    return templates.TemplateResponse(request, "add_guardian.html")

@router.post("/add-guardian", response_class=HTMLResponse)
def add_guardian_submit(
    request: Request,
    guard_id: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    phone: str = Form(...),
):
    
    conn = db.get_db_conn()
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

@router.get("/link-guardian", response_class=HTMLResponse)
def link_guardian_page(request: Request):
    return templates.TemplateResponse(request, "link_guardian.html")

@router.post("/link-guardian", response_class=HTMLResponse)
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
